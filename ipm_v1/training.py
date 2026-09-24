from __future__ import annotations

from dataclasses import dataclass
import math
import time
from typing import Iterable

import numpy as np
import torch

from .core import (
    FrozenProgram,
    IDTC,
    LocalTaylorJet,
    principal_role_coeffs,
    simpson_integral_loss,
)

DEFAULT_STRIDES = (1, 2, 4)


@dataclass
class StandardDataFit:
    model: IDTC
    history: list[dict]
    a_scale: tuple[float, float, float, float]
    q_scale: float
    optimizer_updates: int
    trajectory_exposures: int
    wall_seconds: float
    peak_vram_mb: float


def _require_bnt(data: torch.Tensor) -> None:
    if data.ndim != 3:
        raise ValueError(f"Expected [B,N,T] tensor, got {tuple(data.shape)}")
    if data.shape[-1] < 9:
        raise ValueError("At least 9 time samples are required for strides 1/2/4.")


def _gather_frames(
    data: torch.Tensor,
    traj_ids: torch.Tensor,
    starts: torch.Tensor,
) -> torch.Tensor:
    """Gather one time frame per trajectory from [B,N,T] -> [batch,N]."""
    subset = data.index_select(0, traj_ids)
    idx = starts[:, None, None].expand(-1, subset.shape[1], 1)
    return torch.gather(subset, 2, idx).squeeze(-1)


def estimate_standard_scales(
    train_data: torch.Tensor,
    *,
    length: float,
    dt: float,
    max_trajectories: int = 1024,
    strides: Iterable[int] = DEFAULT_STRIDES,
) -> tuple[torch.Tensor, float]:
    """Estimate frozen jet and characteristic scales from training data only.

    The estimator is deterministic: it takes the first max_trajectories
    training trajectories and deterministic start positions for each stride.
    """
    _require_bnt(train_data)
    device = train_data.device
    dtype = train_data.dtype
    ntraj = min(int(max_trajectories), int(train_data.shape[0]))
    ids = torch.arange(ntraj, device=device)
    jet = LocalTaylorJet(radius=4, degree=5, order=3)

    sum_a2 = torch.zeros(4, device=device, dtype=torch.float64)
    count_a = 0
    sum_q2 = torch.zeros((), device=device, dtype=torch.float64)
    count_q = 0

    with torch.no_grad():
        for s in tuple(int(x) for x in strides):
            max_start = int(train_data.shape[-1]) - 2 * s
            if max_start <= 0:
                raise ValueError(f"Stride {s} is invalid for T={train_data.shape[-1]}")
            # Deterministic, task-independent coverage of the reduced time axis.
            starts = (torch.arange(ntraj, device=device) * (2 * s + 3) + 7 * s) % max_start
            u0 = _gather_frames(train_data, ids, starts)
            u1 = _gather_frames(train_data, ids, starts + s)
            u2 = _gather_frames(train_data, ids, starts + 2 * s)

            frames = torch.cat([u0, u1, u2], dim=0)[:, None, :]
            a = jet(frames, float(length)).double()
            sum_a2 += a.square().sum(dim=(0, 1))
            count_a += int(a.shape[0] * a.shape[1])

            h = float(s) * float(dt)
            secant = ((u2 - u0) / (2.0 * h)).double()
            sum_q2 += secant.square().sum()
            count_q += int(secant.numel())

    a_scale = torch.sqrt(sum_a2 / max(count_a, 1)).to(dtype=dtype)
    a_scale = torch.clamp(a_scale, min=torch.finfo(dtype).eps)
    q_scale = float(torch.sqrt(sum_q2 / max(count_q, 1)).item())
    q_scale = max(q_scale, float(torch.finfo(dtype).eps))
    return a_scale, q_scale


def sampled_simpson_loss(
    model: IDTC,
    jet: LocalTaylorJet,
    train_data: torch.Tensor,
    traj_ids: torch.Tensor,
    *,
    length: float,
    dt: float,
    generator: torch.Generator,
    strides: Iterable[int] = DEFAULT_STRIDES,
) -> torch.Tensor:
    """One architecture-native loss update for a trajectory batch.

    Every trajectory in traj_ids contributes one randomly located Simpson
    triplet for each frozen stride. No exact PDE RHS is used.
    """
    losses = []
    batch = int(traj_ids.numel())
    device = train_data.device

    for s in tuple(int(x) for x in strides):
        max_start = int(train_data.shape[-1]) - 2 * s
        if max_start <= 0:
            raise ValueError(f"Stride {s} is invalid for T={train_data.shape[-1]}")

        starts = torch.randint(
            0,
            max_start,
            (batch,),
            device=device,
            generator=generator,
        )
        u0 = _gather_frames(train_data, traj_ids, starts)
        u1 = _gather_frames(train_data, traj_ids, starts + s)
        u2 = _gather_frames(train_data, traj_ids, starts + 2 * s)

        a0 = jet(u0[:, None, :], float(length))
        a1 = jet(u1[:, None, :], float(length))
        a2 = jet(u2[:, None, :], float(length))

        q0 = model(a0)
        q1 = model(a1)
        q2 = model(a2)

        losses.append(
            simpson_integral_loss(
                u0,
                u1,
                u2,
                q0,
                q1,
                q2,
                float(s) * float(dt),
            )
        )

    return torch.stack(losses).mean()


def fit_idtc_standard_data(
    train_data: torch.Tensor,
    *,
    task: str,
    seed: int,
    length: float,
    dt: float,
    epochs: int = 500,
    batch_size: int = 50,
    learning_rate: float = 1e-3,
    weight_decay: float = 1e-4,
    scheduler_step: int = 100,
    scheduler_gamma: float = 0.5,
    strides: Iterable[int] = DEFAULT_STRIDES,
    scale_trajectories: int = 1024,
    diagnostic_every: int = 25,
) -> StandardDataFit:
    """Fit the frozen 35-scalar IDTC under the PDEBench standard-data schedule.

    The nominal schedule intentionally mirrors the official FNO/U-Net
    trajectory-batch scale: one shuffled pass over all official training
    trajectories per epoch, with the same batch size and epoch count.
    """
    _require_bnt(train_data)
    if train_data.device.type != "cuda":
        raise ValueError("Formal standard-data fit expects the training tensor on CUDA.")

    torch.manual_seed(int(seed))
    torch.cuda.manual_seed_all(int(seed))

    a_scale, q_scale = estimate_standard_scales(
        train_data,
        length=float(length),
        dt=float(dt),
        max_trajectories=int(scale_trajectories),
        strides=strides,
    )

    model = IDTC(
        jet_dim=4,
        rank2=4,
        rank3=2,
        a_scale=a_scale.detach().cpu(),
        q_scale=q_scale,
    ).to(train_data.device)

    jet = LocalTaylorJet(radius=4, degree=5, order=3)
    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=float(learning_rate),
        weight_decay=float(weight_decay),
    )
    scheduler = torch.optim.lr_scheduler.StepLR(
        optimizer,
        step_size=int(scheduler_step),
        gamma=float(scheduler_gamma),
    )

    generator = torch.Generator(device=train_data.device)
    generator.manual_seed(int(seed) + 100003)

    ntraj = int(train_data.shape[0])
    expected_batches = math.ceil(ntraj / int(batch_size))
    history: list[dict] = []
    updates = 0
    trajectory_exposures = 0

    torch.cuda.reset_peak_memory_stats()
    torch.cuda.synchronize()
    t0 = time.perf_counter()

    for epoch in range(1, int(epochs) + 1):
        order = torch.randperm(ntraj, generator=generator, device=train_data.device)
        epoch_losses = []

        for lo in range(0, ntraj, int(batch_size)):
            ids = order[lo : lo + int(batch_size)]
            optimizer.zero_grad(set_to_none=True)

            loss = sampled_simpson_loss(
                model,
                jet,
                train_data,
                ids,
                length=float(length),
                dt=float(dt),
                generator=generator,
                strides=strides,
            )
            if not torch.isfinite(loss):
                raise FloatingPointError(
                    f"{task} seed={seed} non-finite loss at epoch={epoch}, update={updates}"
                )

            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()

            updates += 1
            trajectory_exposures += int(ids.numel())
            epoch_losses.append(float(loss.detach().cpu()))

        scheduler.step()

        if len(epoch_losses) != expected_batches:
            raise RuntimeError("Unexpected number of trajectory batches in an epoch.")

        row = {
            "task": str(task),
            "seed": int(seed),
            "epoch": int(epoch),
            "optimizer_updates": int(updates),
            "trajectory_exposures": int(trajectory_exposures),
            "mean_loss": float(np.mean(epoch_losses)),
            "median_loss": float(np.median(epoch_losses)),
            "lr": float(optimizer.param_groups[0]["lr"]),
        }
        history.append(row)

        if diagnostic_every and (
            epoch == 1
            or epoch == int(epochs)
            or epoch % int(diagnostic_every) == 0
        ):
            print(
                f"[IPM-SD] task={task} seed={seed} epoch={epoch}/{epochs} "
                f"updates={updates} loss={row['mean_loss']:.6g} lr={row['lr']:.3g}"
            )

    torch.cuda.synchronize()
    wall = time.perf_counter() - t0
    peak = torch.cuda.max_memory_allocated() / 2**20

    return StandardDataFit(
        model=model.eval(),
        history=history,
        a_scale=tuple(float(x) for x in a_scale.detach().cpu().tolist()),
        q_scale=float(q_scale),
        optimizer_updates=int(updates),
        trajectory_exposures=int(trajectory_exposures),
        wall_seconds=float(wall),
        peak_vram_mb=float(peak),
    )


def compile_dense_program(
    model: IDTC,
    *,
    task: str,
    seed: int,
) -> FrozenProgram:
    """Compile IDTC to the principal normal form without equation-specific pruning.

    The dense RTDS mask is deliberate for the public same-data fairness track:
    no known target PDE structure is used to delete a learned role.
    """
    roles = principal_role_coeffs(model)
    coeffs = {
        role: tuple(float(x) for x in np.asarray(roles[role]).tolist())
        for role in ("R", "T", "D", "S")
    }
    gains = {role: 1.0 for role in ("R", "T", "D", "S")}
    return FrozenProgram(
        task=str(task),
        seed=int(seed),
        mask="RTDS",
        gains=gains,
        coefficients=coeffs,
    )


def role_contribution_rms(
    model: IDTC,
    frames: torch.Tensor,
    *,
    length: float,
) -> dict[str, float]:
    """RMS contribution of each principal role on supplied [B,1,N] frames."""
    if frames.ndim != 3 or frames.shape[1] != 1:
        raise ValueError("frames must have shape [B,1,N]")

    jet = LocalTaylorJet(radius=4, degree=5, order=3)
    a = jet(frames, float(length))
    roles = principal_role_coeffs(model)

    def poly(c, u):
        c = torch.as_tensor(c, device=u.device, dtype=u.dtype)
        return ((c[3] * u + c[2]) * u + c[1]) * u + c[0]

    u = a[..., 0]
    contributions = {
        "R": poly(roles["R"], u),
        "T": poly(roles["T"], u) * a[..., 1],
        "D": poly(roles["D"], u) * a[..., 2],
        "S": poly(roles["S"], u) * a[..., 3],
    }
    q = sum(contributions.values())
    q_rms = q.square().mean().sqrt().clamp_min(1e-12)

    out = {"Q_RMS": float(q_rms.detach().cpu())}
    for role, value in contributions.items():
        rms = value.square().mean().sqrt()
        out[f"{role}_RMS"] = float(rms.detach().cpu())
        out[f"{role}_FRACTION"] = float((rms / q_rms).detach().cpu())
    return out
