# Intrinsic PDE Model (IPM)

> **Research codebase for _Make PDE integrated into model native_**  
> **《Make PDE integrated into model native》论文实验与开源代码仓库**

---

## Current frozen status — 2026-09-23

**IPM-v1 is frozen.** The mathematical core is the Q3-FIX2 principal normal form compiled from the learned differential law, and the deployment runtime is the Q4 CUDA-Graph engine.

- Frozen public PDEBench programs: Advection beta=1 (`T`) and Burgers nu=0.01 (`T+D+S`).
- Historical IDTC discovery core: **35 trainable scalars**.
- Effective compiled program size: **36 scalars** for Advection and **38 scalars** for Burgers.
- Q4 end-to-end single-step speedup vs same-process official NeuralOperator FNO: about **48.8x / 17.5x** at batch 1 and **45.2x / 17.7x** at batch 16.
- The architecture-modification phase is closed; the repository is now in the comprehensive benchmark phase.

### Install the frozen reusable core

```bash
pip install "git+https://github.com/Mr-wuff/IPM-Intrinsic-PDE-Model.git@main"
```

```python
from ipm_v1 import load_program, IPMStep, HorizonCUDAGraph
```

The exact frozen program coefficients are versioned in the repository. **Future benchmark notebooks must import the repository package instead of requiring users to re-upload historical Q0/Q3-FIX2/Q4 result ZIP files.**

See `docs/IPM_V1_CODE_QUICKSTART.md`.

> Note: the first B0 classical-solver harness formally passed, but a post-run audit found a batch-index bug in the constant-velocity semi-Lagrangian baseline. That row is not paper-final; B0-FIX1 is preregistered and uses the corrected repository implementation.

## English

### Overview

**Intrinsic PDE Model (IPM)** is a research project exploring a new neural architecture for partial differential equation (PDE) modeling.

The central idea is simple:

> Instead of treating a PDE only as an external loss, a symbolic condition, or a target operator, can the differential structure of the PDE become part of the model's own state and evolution mechanism?

Conventional neural PDE models often evolve a field state

[
u(x,t)
]

or learn a mapping between solution states. IPM investigates a different state representation based on local differential structure:

[
J^k u
=
left(
u,partial u,partial^2u,ldots,partial^k u
ight),
]

where (J^k u) denotes a finite-order jet state.

The long-term research objective of IPM is to determine whether a model can learn continuous physical dynamics while keeping differential consistency **intrinsic to the architecture**, rather than relying only on external regularization.

---

### Core architectural hypothesis

For an evolution PDE

[
u_t = F(x,t,J^k u),
]

IPM introduces a learnable infinitesimal generator

[
Q_	heta(J^k u,lambda)approx u_t,
]

where (lambda) denotes physical parameters.

The key architectural idea is that the model should not freely predict every derivative-state tendency independently. Instead, higher-order differential evolution is generated from the base generator through an intrinsic prolongation operation:

[
rac{dJ^k u}{dt}
=
operatorname{Prol}^{(k)} Q_	heta.
]

In one spatial dimension,

[
operatorname{Prol}^{(k)} Q_	heta
=
left(
Q_	heta,
D_xQ_	heta,
D_x^2Q_	heta,
ldots,
D_x^kQ_	heta
ight).
]

This creates a distinction between:

- **derivatives as input features**, and
- **differential structure as the model state and transition law**.

A major question of the project is whether this distinction produces measurable advantages in stability, generalization, physical consistency, and data efficiency.

---

### Research questions

IPM is developed around several falsifiable questions:

1. **State representation**  
   Is a differential / jet state more suitable for learning PDE dynamics than a field-only state?

2. **Intrinsic consistency**  
   Does enforcing differential consistency by construction outperform predicting derivative evolution freely or using only a consistency loss?

3. **Continuous-time dynamics**  
   Can IPM learn an infinitesimal generator that transfers across time-step sizes?

4. **Spatial generalization**  
   Can the same learned dynamics transfer across grid resolutions without retraining?

5. **Physical-parameter generalization**  
   Can IPM extrapolate to unseen coefficients, forcing regimes, and initial conditions?

6. **Multi-PDE generalization**  
   Can a shared intrinsic differential representation support transfer across different PDE families?

7. **Efficiency**  
   Can intrinsic structure improve the accuracy–stability–compute trade-off compared with strong neural PDE baselines?

---

### Experimental methodology

Formal experiments follow a preregistered protocol:

- hypothesis and null hypothesis are fixed before training;
- success / failure gates are specified in advance;
- baselines are capacity- and budget-aware;
- all formal claims use multiple random seeds;
- long-horizon rollout is evaluated in addition to one-step error;
- derivative-state consistency is measured explicitly;
- time-step, grid, parameter, initial-condition, and noise shifts are tested;
- failed experiments remain part of the research record;
- every paper-level result must be reproducible from a frozen code version.

---

### Current experiment series

| Stage | Purpose | Status |
|---|---|---|
| **IPM-M0** | Qualify intrinsic prolongation as an architectural mechanism | Completed — structural identity validated; empirical qualification failed, redesign in progress |
| **IPM-M1** | Repair high-order state closure, conditioning, and rollout stability | Formal script released — experiment pending |
| **IPM-A0** | Formal 1-D multi-PDE benchmark | Blocked until M-stage qualification |
| **IPM-A1** | Time/grid/parameter/IC generalization | Planned |
| **IPM-A2** | 2-D PDE and mixed-derivative consistency | Planned |
| **IPM-A3** | Hard physical regimes and long-horizon stability | Planned |
| **IPM-A4** | Multi-PDE generalist model | Planned |
| **Paper Freeze** | Final benchmark, ablation, theory, figures, and reproducibility release | Planned |

The experiment table will be updated continuously as the project progresses.

---

### IPM-M0: first formal qualification

The first formal mechanism experiment compares five architectures:

1. **FieldState** — field-only state;
2. **DerivativeFeature** — derivatives are provided only as input features;
3. **FreeJet** — derivative-state tendencies are predicted independently;
4. **SoftJetConsistency** — free jet evolution with a consistency penalty;
5. **IPM** — only the base generator is learned, while higher derivative-state tendencies are created by intrinsic prolongation.

The controlled PDE suite includes:

- Heat equation;
- Linear advection equation;
- Viscous Burgers equation;
- Allen–Cahn equation;
- Korteweg–de Vries (KdV) equation.

The first M0 run showed an important result: the intrinsic prolongation identity was satisfied numerically, but the full IPM rollout became unstable in high-order and out-of-distribution settings. This means the mathematical constraint itself is implementable, while finite-order state closure, derivative conditioning, and numerical evolution require further redesign before larger experiments.

Negative results are retained intentionally because they define the architecture's actual failure modes and guide the next model revision.

---

### Planned benchmark dimensions

IPM will be evaluated along the following axes:

- one-step prediction;
- long-horizon rollout;
- field error;
- gradient / higher-derivative error;
- jet consistency defect;
- PDE residual as an evaluation metric;
- conservation / invariant drift where applicable;
- spectral and phase error;
- time-step transfer;
- grid-resolution transfer;
- coefficient extrapolation;
- initial- and boundary-condition shifts;
- noisy-observation robustness;
- data efficiency;
- inference latency;
- memory use;
- computational cost.

Public benchmark suites will be added only after the core architecture passes controlled mechanism qualification.

---

### Repository structure

```text
ipm/
  model/
  geometry/
  operators/
  integrators/
  constraints/

experiments/
  IPM-M0/
  IPM-M1/
  IPM-A0/
  ...

benchmarks/
configs/
tests/
docs/
paper/
scripts/
```

Formal experiments use dedicated branches such as:

```text
exp/ipm-m0-intrinsic-prolongation
exp/ipm-m1-holonomic-closure
exp/ipm-a0-1d-benchmark
```

---

### Reproducibility policy

Each formal experiment is expected to export:

```text
config.json
environment.txt
seed_manifest.json
train_metrics.csv
eval_metrics.csv
gates.json
failure_analysis.md
figures/
tables/
checkpoints/
RESULT_MANIFEST.json
```

A result is eligible for the paper only when it can be reproduced from a frozen repository state and passes the experiment's predefined validity checks.

---

### Paper

**Working title**

> **Make PDE integrated into model native**

The paper will focus on the IPM architecture, its mathematical formulation, mechanism ablations, controlled PDE experiments, generalization behavior, computational properties, and reproducibility.

---

## 中文

### 项目简介

**Intrinsic PDE Model（IPM，内生偏微分方程模型）** 是一个面向偏微分方程建模的新型神经网络架构研究项目。

项目最核心的问题是：

> 能否不再仅仅把 PDE 当作模型外部的损失函数、符号条件或预测目标，而是让 PDE 的微分结构直接成为模型自身状态空间与演化机制的一部分？

传统神经 PDE 模型通常直接演化场状态

[
u(x,t)
]

或者学习不同解状态之间的映射。IPM 尝试将模型状态提升为有限阶局部微分状态：

[
J^k u
=
left(
u,partial u,partial^2u,ldots,partial^k u
ight),
]

其中 (J^k u) 表示有限阶射流状态（jet state）。

IPM 的研究目标，是探索一种让微分一致性**内生于模型架构本身**的连续动力学模型，而不是仅依赖外部正则项迫使网络满足物理关系。

---

### 核心架构构想

对于一般演化型 PDE：

[
u_t=F(x,t,J^ku),
]

IPM 学习一个无穷小演化生成元：

[
Q_	heta(J^ku,lambda)approx u_t,
]

其中 (lambda) 表示物理参数。

IPM 的关键区别在于：

模型不允许自由、独立地预测每一阶导数状态的时间演化，而是从基本生成元 (Q_	heta) 出发，通过模型内部的 **Intrinsic Prolongation（内生延拓）** 自动构造整个射流状态的演化：

[
rac{dJ^ku}{dt}
=
operatorname{Prol}^{(k)}Q_	heta.
]

在一维情况下：

[
operatorname{Prol}^{(k)}Q_	heta
=
left(
Q_	heta,
D_xQ_	heta,
D_x^2Q_	heta,
ldots,
D_x^kQ_	heta
ight).
]

因此，本项目重点研究两种本质不同的建模方式：

- **将导数作为额外输入特征；**
- **将微分结构本身作为模型状态与演化规律。**

IPM 是否能够由此获得更好的稳定性、泛化性、物理一致性和数据效率，是整个项目需要通过实验回答的核心科学问题。

---

### 核心研究问题

1. **状态空间问题**  
   相比仅使用场状态 (u)，射流/微分状态是否更适合学习 PDE 动力学？

2. **内生一致性问题**  
   将微分一致性直接写入模型结构，是否优于自由预测导数演化或者仅加入 consistency loss？

3. **连续时间问题**  
   IPM 是否真正学习无穷小生成元，从而能够跨不同时间步长推理？

4. **空间泛化问题**  
   模型能否在不重新训练的情况下跨网格分辨率工作？

5. **物理参数泛化问题**  
   模型能否推广到未见过的系数、外强迫和初始条件？

6. **跨 PDE 泛化问题**  
   一套共享的内生微分状态机制能否支持不同 PDE 家族之间的迁移？

7. **计算效率问题**  
   IPM 能否在精度、稳定性与计算成本之间获得更好的综合表现？

---

### 实验方法

所有正式实验遵循统一科研协议：

- 训练前冻结科学假设与零假设；
- 训练前确定 PASS / FAIL Gate；
- 尽量保证基线参数量、训练预算和数据公平；
- 核心结论采用多随机种子重复；
- 不仅测试单步误差，还测试长时间 rollout；
- 单独评估高阶导数状态与微分一致性；
- 系统测试时间步、网格、参数、初值和噪声分布偏移；
- 失败实验同样保留并归档；
- 论文中的结果必须能够从冻结版本代码复现。

---

### 当前实验路线

| 阶段 | 目标 | 状态 |
|---|---|---|
| **IPM-M0** | 验证 Intrinsic Prolongation 是否具备成为核心架构机制的资格 | 已完成——结构恒等性成立，但经验性能资格验证失败，正在重新设计 |
| **IPM-M1** | 解决高阶状态闭合、条件数与 rollout 稳定性问题 | 正式脚本已发布——等待实验结果 |
| **IPM-A0** | 正式一维多 PDE Benchmark | 等待 M 阶段通过 |
| **IPM-A1** | 时间步/网格/参数/初值泛化实验 | 计划中 |
| **IPM-A2** | 二维 PDE 与混合偏导一致性 | 计划中 |
| **IPM-A3** | 困难物理区间与长期演化稳定性 | 计划中 |
| **IPM-A4** | 多 PDE 通用模型 | 计划中 |
| **论文冻结** | 最终 Benchmark、消融、理论、图表和复现发布 | 计划中 |

该表将随着实验推进持续更新。

---

### IPM-M0：第一轮正式机制实验

IPM-M0 对比五类模型：

1. **FieldState**：仅使用场状态；
2. **DerivativeFeature**：导数仅作为输入特征；
3. **FreeJet**：自由预测所有射流分量的演化；
4. **SoftJetConsistency**：自由射流演化 + 一致性损失；
5. **IPM**：仅学习基本生成元，高阶导数演化由 Intrinsic Prolongation 内生生成。

受控 PDE 测试集合包括：

- 热方程（Heat equation）；
- 线性平流方程（Linear advection）；
- 黏性 Burgers 方程；
- Allen–Cahn 方程；
- Korteweg–de Vries（KdV）方程。

第一轮 M0 的结果表明：Intrinsic Prolongation 的结构恒等关系可以数值实现，但当前 IPM 在高阶状态演化和分布外测试中的 rollout 稳定性不足。

因此当前研究重点转向有限阶微分状态闭合、高阶导数条件数以及数值演化稳定性的重新设计，而不是直接扩大模型规模。

项目会保留这些失败结果，因为失败边界本身也是确定新架构是否真正成立的重要科研证据。

---

### 后续评价维度

IPM 将逐步覆盖：

- 单步预测误差；
- 长时间 rollout；
- 场值误差；
- 梯度与高阶导数误差；
- 射流一致性缺陷；
- PDE residual（作为评价指标）；
- 守恒量与不变量漂移；
- 频谱误差；
- 相位误差；
- 时间步迁移；
- 空间分辨率迁移；
- 物理参数外推；
- 初始/边界条件迁移；
- 噪声鲁棒性；
- 数据效率；
- 推理延迟；
- 显存占用；
- 计算成本。

只有在核心机制资格验证通过后，才进入更大规模的公开 Benchmark。

---

### 仓库结构

```text
ipm/
  model/
  geometry/
  operators/
  integrators/
  constraints/

experiments/
  IPM-M0/
  IPM-M1/
  IPM-A0/
  ...

benchmarks/
configs/
tests/
docs/
paper/
scripts/
```

正式实验使用独立实验分支，例如：

```text
exp/ipm-m0-intrinsic-prolongation
exp/ipm-m1-holonomic-closure
exp/ipm-a0-1d-benchmark
```

---

### 可复现性规范

每轮正式实验计划统一导出：

```text
config.json
environment.txt
seed_manifest.json
train_metrics.csv
eval_metrics.csv
gates.json
failure_analysis.md
figures/
tables/
checkpoints/
RESULT_MANIFEST.json
```

只有能够从冻结仓库版本完整复现，并通过预定义有效性检查的实验结果，才会进入论文正文。

---

### 论文

**暂定题目**

> **Make PDE integrated into model native**

论文将集中讨论 IPM 的数学定义、核心架构、机制消融、受控 PDE 实验、泛化能力、计算特性以及完整复现流程。
