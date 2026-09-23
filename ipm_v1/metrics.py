from __future__ import annotations
import torch

def rel_l2(pred,true,eps=1e-12):
    if not torch.isfinite(pred).all(): return float("inf")
    return float(((pred-true).pow(2).mean().sqrt()/
                  true.pow(2).mean().sqrt().clamp_min(eps)).item())

def rmse(pred,true):
    if not torch.isfinite(pred).all(): return float("inf")
    return float((pred-true).pow(2).mean().sqrt().item())

def rollout(step,u0,steps):
    x=u0
    outs=[]
    for _ in range(int(steps)):
        x=step(x)
        outs.append(x)
    return torch.stack(outs,dim=1)
