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


def test_standard_data_scale_and_dense_compile_cpu():
    from ipm_v1.core import IDTC
    from ipm_v1.training import estimate_standard_scales, compile_dense_program
    torch.manual_seed(11)
    data=torch.randn(16,64,17,dtype=torch.float32)
    a_scale,q_scale=estimate_standard_scales(
        data,length=1.0,dt=0.05,max_trajectories=8
    )
    assert a_scale.shape==(4,)
    assert bool(torch.isfinite(a_scale).all())
    assert q_scale>0

    model=IDTC(a_scale=a_scale,q_scale=q_scale)
    program=compile_dense_program(model,task="synthetic",seed=11)
    assert program.mask=="RTDS"
    assert set(program.coefficients)=={"R","T","D","S"}


def test_runtime_applies_principal_role_gains_cpu():
    from ipm_v1.core import FrozenProgram

    torch.manual_seed(19)
    u=torch.randn(5,1,96)
    coeffs={
        "R":(0.03,-0.02,0.0,0.0),
        "T":(-0.4,0.1,0.0,0.0),
        "D":(0.02,0.0,0.0,0.0),
        "S":(0.001,0.0,0.0,0.0),
    }
    gains={"R":0.25,"T":1.7,"D":2.2,"S":-0.6}
    p_gain=FrozenProgram("synthetic",1,"RTDS",gains,coeffs)

    # Folding a scalar role gain into every coefficient of that role is
    # mathematically identical to applying the gain at runtime.
    folded={
        role:tuple(float(gains[role])*float(v) for v in coeffs[role])
        for role in ("R","T","D","S")
    }
    p_fold=FrozenProgram(
        "synthetic",1,"RTDS",
        {"R":1.0,"T":1.0,"D":1.0,"S":1.0},
        folded,
    )

    m_gain=IPMStep(p_gain,96,1.0,1e-3)
    m_fold=IPMStep(p_fold,96,1.0,1e-3)
    y_gain=m_gain(u)
    y_fold=m_fold(u)

    rel=((y_gain-y_fold).pow(2).mean().sqrt()/
         y_fold.pow(2).mean().sqrt().clamp_min(1e-12))
    assert float(rel)<2e-6


def test_nonunit_gain_changes_runtime_cpu():
    from ipm_v1.core import FrozenProgram

    torch.manual_seed(23)
    u=torch.randn(4,1,64)
    coeffs={
        "R":(0.0,0.0,0.0,0.0),
        "T":(-0.5,0.0,0.0,0.0),
        "D":(0.0,0.0,0.0,0.0),
        "S":(0.0,0.0,0.0,0.0),
    }
    unit=FrozenProgram(
        "synthetic",1,"T",
        {"R":0.0,"T":1.0,"D":0.0,"S":0.0},
        coeffs,
    )
    double=FrozenProgram(
        "synthetic",1,"T",
        {"R":0.0,"T":2.0,"D":0.0,"S":0.0},
        coeffs,
    )
    y1=IPMStep(unit,64,1.0,1e-2)(u)
    y2=IPMStep(double,64,1.0,1e-2)(u)
    rel=((y1-y2).pow(2).mean().sqrt()/
         y1.pow(2).mean().sqrt().clamp_min(1e-12))
    assert float(rel)>1e-4
