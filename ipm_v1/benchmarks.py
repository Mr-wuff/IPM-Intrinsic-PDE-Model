from __future__ import annotations
import math
import torch
import torch.nn as nn

def minmod(a,b):
    same=(a*b)>0
    return torch.where(same,torch.sign(a)*torch.minimum(a.abs(),b.abs()),torch.zeros_like(a))

class AdvFourierExact(nn.Module):
    def __init__(self,n,length,dt,beta=1.0):
        super().__init__(); self.n=int(n)
        k=2*math.pi*torch.fft.rfftfreq(self.n,d=float(length)/self.n)
        self.register_buffer("phase",torch.exp((-1j*beta*k*dt).to(torch.complex64)))
    def forward(self,u):
        return torch.fft.irfft(torch.fft.rfft(u,dim=-1)*self.phase,n=self.n,dim=-1).real

class AdvSemiLagrangian(nn.Module):
    """Periodic constant-velocity semi-Lagrangian baseline.

    The index grid is explicitly expanded to the input batch. This fixes the
    initial B0 harness bug where torch.gather collapsed a B>1 accuracy batch.
    """
    def __init__(self,n,length,dt,beta=1.0):
        super().__init__(); self.n=int(n)
        self.shift=float(beta*dt/(float(length)/self.n))
        self.register_buffer("grid",torch.arange(self.n,dtype=torch.float32)[None,None,:])
    def forward(self,u):
        grid=self.grid.to(u.dtype).expand(u.shape[0],-1,-1)
        pos=grid-self.shift
        j0=torch.floor(pos).long()
        frac=pos-j0.to(pos.dtype)
        j0=torch.remainder(j0,self.n)
        j1=torch.remainder(j0+1,self.n)
        return (1-frac)*torch.gather(u,-1,j0)+frac*torch.gather(u,-1,j1)

class AdvUpwind(nn.Module):
    def __init__(self,n,length,dt,beta=1.0,substeps=1):
        super().__init__(); self.beta=float(beta); self.h=float(dt)/substeps
        self.dx=float(length)/n; self.substeps=int(substeps)
        self.c=self.beta*self.h/self.dx
    def forward(self,u):
        x=u
        for _ in range(self.substeps):
            if self.beta>=0:
                x=x-self.c*(x-torch.roll(x,1,dims=-1))
            else:
                x=x-self.c*(torch.roll(x,-1,dims=-1)-x)
        return x

class AdvLaxWendroff(nn.Module):
    def __init__(self,n,length,dt,beta=1.0,substeps=1):
        super().__init__(); self.h=float(dt)/substeps; self.dx=float(length)/n
        self.substeps=int(substeps); self.c=float(beta)*self.h/self.dx
    def forward(self,u):
        x=u; c=self.c
        for _ in range(self.substeps):
            xp=torch.roll(x,-1,dims=-1); xm=torch.roll(x,1,dims=-1)
            x=x-0.5*c*(xp-xm)+0.5*c*c*(xp-2*x+xm)
        return x

class BurgersBase(nn.Module):
    def __init__(self,n,length,dt,nu=0.01,substeps=1):
        super().__init__(); self.n=int(n); self.length=float(length); self.dt=float(dt)
        self.nu=float(nu); self.substeps=int(substeps); self.h=self.dt/self.substeps
        self.dx=self.length/self.n
        k=2*math.pi*torch.fft.rfftfreq(self.n,d=self.dx)
        self.register_buffer("k",k.float())
    def diffuse(self,u,h):
        U=torch.fft.rfft(u,dim=-1); k=self.k.to(u.dtype)
        return torch.fft.irfft(U*torch.exp(-self.nu*k.square()*h),n=self.n,dim=-1).real

class BurgersSL(BurgersBase):
    def __init__(self,n,length,dt,nu=0.01,substeps=1):
        super().__init__(n,length,dt,nu,substeps)
        self.register_buffer("grid",torch.arange(self.n,dtype=torch.float32)[None,None,:])
    def transport(self,u,h):
        pos=self.grid.to(u.dtype)-u*h/self.dx
        j0=torch.floor(pos).long(); frac=pos-j0.to(pos.dtype)
        j0=torch.remainder(j0,self.n); j1=torch.remainder(j0+1,self.n)
        return (1-frac)*torch.gather(u,-1,j0)+frac*torch.gather(u,-1,j1)
    def forward(self,u):
        x=u
        for _ in range(self.substeps):
            x=self.diffuse(x,0.5*self.h); x=self.transport(x,self.h); x=self.diffuse(x,0.5*self.h)
        return x

class BurgersRusanov(BurgersBase):
    def flux_rhs(self,u):
        ur=torch.roll(u,-1,dims=-1)
        fl=0.5*u.square(); fr=0.5*ur.square()
        a=torch.maximum(u.abs(),ur.abs())
        Fh=0.5*(fl+fr)-0.5*a*(ur-u)
        return -(Fh-torch.roll(Fh,1,dims=-1))/self.dx
    def convect_ssprk3(self,u,h):
        k1=self.flux_rhs(u); u1=u+h*k1
        k2=self.flux_rhs(u1); u2=0.75*u+0.25*(u1+h*k2)
        k3=self.flux_rhs(u2)
        return (1/3)*u+(2/3)*(u2+h*k3)
    def forward(self,u):
        x=u
        for _ in range(self.substeps):
            x=self.diffuse(x,0.5*self.h); x=self.convect_ssprk3(x,self.h); x=self.diffuse(x,0.5*self.h)
        return x

class BurgersMUSCLRusanov(BurgersRusanov):
    def flux_rhs(self,u):
        db=u-torch.roll(u,1,dims=-1); df=torch.roll(u,-1,dims=-1)-u
        slope=minmod(db,df)
        uL=u+0.5*slope
        uR=torch.roll(u,-1,dims=-1)-0.5*torch.roll(slope,-1,dims=-1)
        fL=0.5*uL.square(); fR=0.5*uR.square()
        a=torch.maximum(uL.abs(),uR.abs())
        Fh=0.5*(fL+fR)-0.5*a*(uR-uL)
        return -(Fh-torch.roll(Fh,1,dims=-1))/self.dx

class BurgersPseudoSpectral(BurgersBase):
    def nonlinear_rhs(self,u):
        flux=0.5*u.square()
        Fh=torch.fft.rfft(flux,dim=-1)
        cutoff=self.n//3
        mask=(torch.arange(Fh.shape[-1],device=u.device)<=cutoff).to(Fh.dtype)
        Fh=Fh*mask
        k=self.k.to(u.dtype)
        dflux=torch.fft.irfft(Fh*(1j*k).to(Fh.dtype),n=self.n,dim=-1).real
        return -dflux
    def convect_rk4(self,u,h):
        k1=self.nonlinear_rhs(u)
        k2=self.nonlinear_rhs(u+0.5*h*k1)
        k3=self.nonlinear_rhs(u+0.5*h*k2)
        k4=self.nonlinear_rhs(u+h*k3)
        return u+(h/6)*(k1+2*k2+2*k3+k4)
    def forward(self,u):
        x=u
        for _ in range(self.substeps):
            x=self.diffuse(x,0.5*self.h); x=self.convect_rk4(x,self.h); x=self.diffuse(x,0.5*self.h)
        return x
