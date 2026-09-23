from __future__ import annotations
from dataclasses import dataclass
from importlib import resources
from itertools import combinations_with_replacement
import json, math
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

ROLES=("R","T","D","S")

@dataclass(frozen=True)
class FrozenProgram:
    task: str
    seed: int
    mask: str
    gains: dict[str,float]
    coefficients: dict[str,tuple[float,float,float,float]]

    @property
    def effective_scalar_count(self) -> int:
        return 35 + len(self.mask)

def _program_db():
    return json.loads(resources.files("ipm_v1").joinpath("programs.json").read_text(encoding="utf-8"))

def load_program(task: str, seed: int = 202) -> FrozenProgram:
    db=_program_db()
    payload=db[task][str(int(seed))]
    coeffs={r:tuple(float(x) for x in payload["coefficients"][r]) for r in ROLES}
    gains={r:float(payload["gains"][r]) for r in ROLES}
    return FrozenProgram(task,int(seed),str(payload["mask"]),gains,coeffs)

def available_programs():
    db=_program_db()
    return sorted((task,int(seed)) for task,v in db.items() for seed in v)

def local_taylor_base_weights(radius=4, degree=5, order=3):
    s=np.arange(-radius,radius+1,dtype=np.float64)
    V=np.stack([s**j for j in range(degree+1)],axis=1)
    P=np.linalg.pinv(V)
    return torch.tensor(np.stack([P[r] for r in range(order+1)]),dtype=torch.float64)

class LocalTaylorJet:
    """Fast local Taylor jet used during Q2 discovery, not required by frozen deployment."""
    def __init__(self,radius=4,degree=5,order=3):
        self.radius=int(radius); self.degree=int(degree); self.order=int(order)
        self.base=local_taylor_base_weights(radius,degree,order)
    def __call__(self,u,length:float):
        if u.ndim==2: u=u[:,None,:]
        n=u.shape[-1]; dx=float(length)/n
        scales=torch.tensor([dx**(-r) for r in range(self.order+1)],device=u.device,dtype=u.dtype)
        kernel=(self.base.to(u.device,u.dtype)*scales[:,None])[:,None,:]
        up=F.pad(u,(self.radius,self.radius),mode="circular")
        return F.conv1d(up,kernel).permute(0,2,1).contiguous()

class IDTC(nn.Module):
    """35-parameter Intrinsic Differential Tensor Core.

    Q(z)=q_s[b+w^Tz+sum alpha_m(v_m^Tz)^2+sum beta_n(r_n^Tz)^3]
    with jet_dim=4, R2=4, R3=2 -> 35 trainable scalars.
    """
    def __init__(self,jet_dim=4,rank2=4,rank3=2,a_scale=None,q_scale=1.0):
        super().__init__()
        self.bias=nn.Parameter(torch.zeros(()))
        self.linear=nn.Parameter(torch.zeros(jet_dim))
        self.v2=nn.Parameter(torch.randn(rank2,jet_dim)*0.02)
        self.a2=nn.Parameter(torch.zeros(rank2))
        self.v3=nn.Parameter(torch.randn(rank3,jet_dim)*0.02)
        self.a3=nn.Parameter(torch.zeros(rank3))
        if a_scale is None: a_scale=torch.ones(jet_dim)
        self.register_buffer("a_scale",torch.as_tensor(a_scale,dtype=torch.float32))
        self.register_buffer("q_scale",torch.tensor(float(q_scale),dtype=torch.float32))
    def forward(self,a):
        z=a/self.a_scale.to(a.device,a.dtype).clamp_min(1e-8)
        q=self.bias+torch.einsum("...d,d->...",z,self.linear)
        p2=torch.einsum("...d,rd->...r",z,self.v2)
        q=q+torch.einsum("...r,r->...",p2.square(),self.a2)
        p3=torch.einsum("...d,rd->...r",z,self.v3)
        q=q+torch.einsum("...r,r->...",p3.pow(3),self.a3)
        return self.q_scale.to(a.device,a.dtype)*q

def canonical_terms(model: IDTC):
    s=model.a_scale.detach().cpu().double().numpy()
    qs=float(model.q_scale.detach().cpu())
    lin=model.linear.detach().cpu().double().numpy()
    V2=model.v2.detach().cpu().double().numpy()
    A2=model.a2.detach().cpu().double().numpy()
    V3=model.v3.detach().cpu().double().numpy()
    A3=model.a3.detach().cpu().double().numpy()
    terms={(0,0,0,0):qs*float(model.bias.detach().cpu())}
    for i,c in enumerate(qs*lin/s):
        e=[0,0,0,0]; e[i]=1; terms[tuple(e)]=terms.get(tuple(e),0.0)+float(c)
    A=np.zeros((4,4),dtype=np.float64)
    for amp,v in zip(A2,V2):
        vv=v/s; A+=qs*amp*np.outer(vv,vv)
    for i in range(4):
        for j in range(i,4):
            e=[0,0,0,0]; e[i]+=1; e[j]+=1
            terms[tuple(e)]=terms.get(tuple(e),0.0)+float(A[i,j]*(1 if i==j else 2))
    B=np.zeros((4,4,4),dtype=np.float64)
    for amp,v in zip(A3,V3):
        vv=v/s; B+=qs*amp*np.einsum("i,j,k->ijk",vv,vv,vv)
    for i,j,k in combinations_with_replacement(range(4),3):
        mult=1 if i==j==k else (3 if i==j or j==k else 6)
        e=[0,0,0,0]; e[i]+=1; e[j]+=1; e[k]+=1
        terms[tuple(e)]=terms.get(tuple(e),0.0)+float(mult*B[i,j,k])
    return {e:c for e,c in terms.items() if abs(c)>1e-18}

def principal_role_coeffs(model: IDTC):
    roles={r:np.zeros(4,dtype=np.float64) for r in ROLES}
    for exp,coef in canonical_terms(model).items():
        active=[i for i in (1,2,3) if exp[i]>0]
        if not active and exp[0]<=3:
            roles["R"][exp[0]]+=coef
        elif len(active)==1:
            r=active[0]
            if exp[r]==1 and exp[0]<=3:
                roles[{1:"T",2:"D",3:"S"}[r]][exp[0]]+=coef
    return roles

def cartan_dx(value,a,ell=1.0,create_graph=True):
    """D_x F=sum_r ((r+1)/ell) a_{r+1} dF/da_r in 1-D Taylor coordinates."""
    grad=torch.autograd.grad(value.sum(),a,create_graph=create_graph,retain_graph=True)[0]
    out=torch.zeros_like(value)
    for r in range(a.shape[-1]-1):
        out=out+((r+1)/float(ell))*a[...,r+1]*grad[...,r]
    return out

def evolutionary_field_components(q_fn,a,order,ell=1.0):
    """Taylor-coordinate components of V_Q=sum_r ell^r/r! D_x^r Q d/da_r."""
    if not a.requires_grad: a=a.requires_grad_(True)
    q=q_fn(a); comps=[q]; current=q
    for r in range(1,int(order)+1):
        current=cartan_dx(current,a,ell,True)
        comps.append((float(ell)**r/math.factorial(r))*current)
    return comps

def simpson_integral_residual(u0,u1,u2,q0,q1,q2,h):
    return (u2-u0)-(h/3.0)*(q0+4.0*q1+q2)

def simpson_integral_loss(u0,u1,u2,q0,q1,q2,h,eps=1e-8):
    r=simpson_integral_residual(u0,u1,u2,q0,q1,q2,h)
    scale=(u2-u0).pow(2).mean().sqrt().detach().clamp_min(eps)
    return (r/scale).pow(2).mean()
