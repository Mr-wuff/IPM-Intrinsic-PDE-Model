from __future__ import annotations
import math
import torch
import torch.nn as nn
from .core import FrozenProgram, load_program

class IPMStep(nn.Module):
    """Exact frozen Q3-FIX2 principal-normal-form physical step."""
    def __init__(self, program: FrozenProgram, n: int, length: float, dt: float):
        super().__init__()
        self.mask=program.mask
        self.n=int(n)
        self.length=float(length)
        self.dt=float(dt)
        self.dx=self.length/self.n
        for role in ("R","T","D","S"):
            self.register_buffer(f"c_{role}",torch.tensor(program.coefficients[role],dtype=torch.float32))
        self.register_buffer("grid",torch.arange(self.n,dtype=torch.float32)[None,None,:])
        k=2*math.pi*torch.fft.rfftfreq(self.n,d=self.dx)
        self.register_buffer("k",k.float())

    @staticmethod
    def horner(u,c):
        return ((c[3]*u+c[2])*u+c[1])*u+c[0]

    def reaction(self,u,h):
        if "R" not in self.mask: return u
        c=self.c_R.to(u.dtype)
        k1=self.horner(u,c); k2=self.horner(u+h*k1,c)
        return u+0.5*h*(k1+k2)

    def transport(self,u):
        if "T" not in self.mask: return u
        velocity=-self.horner(u,self.c_T.to(u.dtype))
        pos=self.grid.to(u.dtype)-velocity*(self.dt/self.dx)
        j0=torch.floor(pos).long()
        frac=pos-j0.to(pos.dtype)
        j0=torch.remainder(j0,self.n)
        j1=torch.remainder(j0+1,self.n)
        return (1-frac)*torch.gather(u,-1,j0)+frac*torch.gather(u,-1,j1)

    def forward(self,u):
        x=self.reaction(u,0.5*self.dt)
        x=self.transport(x)
        use_d="D" in self.mask
        use_s="S" in self.mask
        if use_d or use_s:
            if use_d:
                f2=self.horner(x,self.c_D.to(x.dtype))
                nu=torch.median(torch.clamp(f2/2.0,min=0.0),dim=-1,keepdim=True).values
            else:
                nu=torch.zeros(x.shape[0],1,1,device=x.device,dtype=x.dtype)
            if use_s:
                f3=self.horner(x,self.c_S.to(x.dtype))
                gamma=torch.median(f3/6.0,dim=-1,keepdim=True).values
            else:
                gamma=torch.zeros(x.shape[0],1,1,device=x.device,dtype=x.dtype)
            U=torch.fft.rfft(x,dim=-1)
            k=self.k.to(x.dtype)

            # Mathematically identical to
            #   exp(dt * (-nu*k^2 + gamma*(i*k)^3))
            # but avoids torch.exp(complex), whose CUDA Jiterator path can
            # require an NVRTC-builtins soname that is absent/mismatched in
            # some Colab images. Since (i*k)^3 = -i*k^3,
            #
            #   exp(-dt*nu*k^2 - i*dt*gamma*k^3)
            # = exp(-dt*nu*k^2) * [cos(phi) - i sin(phi)].
            #
            # This is a runtime-equivalent implementation patch only; it
            # does not alter the frozen PDE program or learned coefficients.
            kk=k[None,None,:]
            decay=torch.exp(-self.dt*nu*kk.square())
            phi=self.dt*gamma*kk.pow(3)
            multiplier=torch.complex(
                decay*torch.cos(phi),
                -decay*torch.sin(phi),
            ).to(U.dtype)
            x=torch.fft.irfft(U*multiplier,n=self.n,dim=-1).real
        return self.reaction(x,0.5*self.dt)

def build_step(task,n,length,dt,seed=202,device=None):
    module=IPMStep(load_program(task,seed),n=n,length=length,dt=dt)
    if device is not None: module=module.to(device)
    return module.eval()

class StepCUDAGraph:
    def __init__(self,module,sample):
        if not sample.is_cuda: raise ValueError("StepCUDAGraph requires CUDA.")
        self.module=module
        self.state=sample.clone()
        side=torch.cuda.Stream()
        side.wait_stream(torch.cuda.current_stream())
        with torch.cuda.stream(side):
            for _ in range(5):
                y=self.module(self.state); self.state.copy_(y)
        torch.cuda.current_stream().wait_stream(side)
        torch.cuda.synchronize()
        self.graph=torch.cuda.CUDAGraph()
        with torch.cuda.graph(self.graph):
            y=self.module(self.state); self.state.copy_(y)
        torch.cuda.synchronize()
    def reset(self,x): self.state.copy_(x)
    def replay(self):
        self.graph.replay()
        return self.state

class HorizonCUDAGraph:
    def __init__(self,module,sample,steps=40):
        if not sample.is_cuda: raise ValueError("HorizonCUDAGraph requires CUDA.")
        self.module=module
        self.state=sample.clone()
        self.steps=int(steps)
        side=torch.cuda.Stream()
        side.wait_stream(torch.cuda.current_stream())
        with torch.cuda.stream(side):
            for _ in range(3):
                y=self.module(self.state); self.state.copy_(y)
        torch.cuda.current_stream().wait_stream(side)
        torch.cuda.synchronize()
        self.graph=torch.cuda.CUDAGraph()
        with torch.cuda.graph(self.graph):
            for _ in range(self.steps):
                y=self.module(self.state); self.state.copy_(y)
        torch.cuda.synchronize()
    def reset(self,x): self.state.copy_(x)
    def replay(self):
        self.graph.replay()
        return self.state
