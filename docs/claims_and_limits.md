# VIREON TRP: Claims, Proofs, and Limits

This repo is **math-first**. It separates:

- What is *proved* in the current code and docs.
- What is only a *hypothesis* (falsifiable, not assumed true).

## 1. Proved in this repo

These are standard theorems or direct consequences of the definitions,
with checks in `tests/`:

1. **KL divergence invariants**
   - `kl_div(p, q) ≥ 0` and `kl_div(p, p) ≈ 0`.
   - Code: `vireon_trp_mip.kl_leash.kl_div`.
   - Tests: `tests/test_math_invariants.py`.

2. **KL-leash non-increase**
   - For any `q_ref`, `q_new`, the leashed distribution `q_leashed`
     satisfies
     \[
     D_\text{KL}(q^\text{leash} \parallel q_\text{ref})
     \le
     D_\text{KL}(q_\text{new} \parallel q_\text{ref}).
     \]
   - Encoded via convex combination and tested numerically.

3. **Red-zone clamp**
   - In the red regime, the code clamps divergence so that
     \[
     D_\text{KL}(q^\text{leash} \parallel q_\text{ref})
     \le \varepsilon_\text{green}.
     \]
   - See `docs/math_foundations.md`, `docs/theorems_kl_leash.md`.

4. **TRP state invariants**
   - If `R_0 ≥ 0`, `P_0 > 0`, and `loss_t ≥ 0`, then
     - `R_t ≥ 0` for all t.
     - `P_t` stays > 0 and non-increasing.
     - Effective time
       \[
       dt_\text{eff}(t) = \frac{1}{1 + R_t P_t}
       \]
       satisfies `0 < dt_eff ≤ 1`.
   - Tested in `tests/test_trp_state.py`.

5. **CollapseTracker behavior**
   - Any region with no improvement larger than `min_improvement` for
     `window` consecutive steps will trigger `collapsed = True`.
   - Tested in `tests/test_math_invariants.py::test_collapse_tracker_triggers_after_window`.

These are **mathematical properties**, not performance claims.

## 2. What the toy solver actually demonstrates

The toy environment in `toy_solver.py` is a **synthetic search tree**.

Scripts:

- `scripts/run_toy_baseline.py`
- `scripts/run_toy_vireon.py`
- `scripts/run_toy_stats.py`

These scripts let anyone measure:

- Node counts and best values for baseline vs VIREON on a controlled problem.
- Whether TRP + KL-leash + collapse helps or hurts on this toy.

The repo does **not** assert any fixed win here:
numbers are empirical and determined by running the code.

## 3. Hypotheses (not yet proved here)

These are the big, falsifiable claims that go beyond this repo:

1. **MIPLIB 2017 Crucible**
   - ≥100× node reduction, ≥10× runtime speedup,
     robustness floor, and volatility reduction.
   - Defined precisely in `docs/crucible_spec.md`.
   - **Not implemented or validated here.**

2. **General 100–1000× search reduction**
   - Conjecture that TRP + KL-leash + collapse can give
     order-of-magnitude improvements on real combinatorial search
     when correctly integrated into strong solvers.
   - This repo provides the **control law**, not the proof
     on real MIP instances.

## 4. How to use this repo as a critic

If you are skeptical, you can:

1. Verify the math:
   - Read `docs/math_foundations.md`, `docs/theorems_kl_leash.md`.
   - Inspect implementations in `src/vireon_trp_mip/`.
   - Run `pytest` to check consistency.

2. Stress-test the toy solver:
   - Change depth, noise, seeds.
   - Compare `run_toy_stats.py` outputs.
   - Look for regimes where VIREON is worse or better.

3. Plug into a real solver:
   - Implement an adapter under `src/vireon_trp_mip/mip/`.
   - Run your own benchmarks and publish results.

## 5. Non-claims

This repo does **not** claim:

- To have already solved MIPLIB 2017 with 100× node reductions.
- To guarantee performance gains on every problem.
- To provide a black-box magic trick.

It **does** claim:

- The mathematical control law is explicit and correct as written.
- The code exactly matches the equations.
- The Crucible protocol gives a clean way to falsify the strong claims.
