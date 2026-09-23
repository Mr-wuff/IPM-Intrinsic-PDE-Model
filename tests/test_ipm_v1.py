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
