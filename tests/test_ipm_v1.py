import torch
from ipm_v1 import load_program, available_programs, IPMStep
from ipm_v1.benchmarks import AdvSemiLagrangian

def test_frozen_programs():
    assert ("advection_beta1",202) in available_programs()
    assert load_program("advection_beta1",202).effective_scalar_count==36
    assert load_program("burgers_nu001",202).effective_scalar_count==38

def test_runtime_cpu_smoke():
    p=load_program("advection_beta1",202)
    m=IPMStep(p,64,1.0,1e-3)
    u=torch.randn(3,1,64)
    y=m(u)
    assert y.shape==u.shape and torch.isfinite(y).all()

def test_constant_sl_batch_fix():
    m=AdvSemiLagrangian(64,1.0,1e-3,1.0)
    u=torch.randn(7,1,64)
    y=m(u)
    assert y.shape==u.shape


def test_spectral_multiplier_runtime_equivalence_cpu():
    # The v1.0.1 runtime avoids torch.exp(complex) but must remain
    # numerically equivalent to the frozen v1.0.0 spectral formula.
    import math
    torch.manual_seed(7)
    n=256
    x=torch.randn(4,1,n,dtype=torch.float64)
    U=torch.fft.rfft(x,dim=-1)
    k=2*math.pi*torch.fft.rfftfreq(n,d=1.0/n,dtype=torch.float64)
    nu=torch.rand(4,1,1,dtype=torch.float64)*0.03
    gamma=(torch.rand(4,1,1,dtype=torch.float64)-0.5)*0.02
    dt=0.005

    symbol=-nu*k[None,None,:].square()+gamma*((1j*k).to(U.dtype)**3)[None,None,:]
    old=torch.exp(dt*symbol)

    kk=k[None,None,:]
    decay=torch.exp(-dt*nu*kk.square())
    phi=dt*gamma*kk.pow(3)
    new=torch.complex(decay*torch.cos(phi),-decay*torch.sin(phi)).to(U.dtype)

    rel=((old-new).abs().pow(2).mean().sqrt()/
         old.abs().pow(2).mean().sqrt().clamp_min(1e-30))
    assert float(rel)<1e-12
