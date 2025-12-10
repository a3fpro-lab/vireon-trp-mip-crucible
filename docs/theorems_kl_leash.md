# KL-Leash Guarantees (Code ↔ Math)

Let q_ref be a fixed distribution and q_new a proposal.
Define
\[
\Delta = D_\text{KL}(q_\text{new} \parallel q_\text{ref}).
\]

In code (`apply_kl_leash`):

- Compute `delta = kl_div(q_new, q_ref)`.
- Compute λ = λ(Δ) as in `docs/math_foundations.md`.
- Output
  \[
  q^\text{leash} = \lambda q_\text{new} + (1-\lambda) q_\text{ref}.
  \]

## Theorem 1 (KL non-increase)

For any q_ref, q_new:

\[
D_\text{KL}(q^\text{leash} \parallel q_\text{ref})
\le
D_\text{KL}(q_\text{new} \parallel q_\text{ref}).
\]

**Reason:** q^\text{leash} is a convex combination of q_new and q_ref, and
KL(·‖q_ref) is convex in the first argument with minimum at q_ref.

Code check: `tests/test_math_invariants.py::test_kl_leash_reduces_divergence`.

## Theorem 2 (Red regime clamp)

In the red regime (Δ ≥ ε_yellow), code sets
\[
\lambda = \varepsilon_\text{green} / \Delta.
\]

Then
\[
D_\text{KL}(q^\text{leash} \parallel q_\text{ref})
\le \varepsilon_\text{green}.
\]

So large proposal jumps are always clamped back to a bounded divergence.

## Theorem 3 (State invariants)

Given R_0 ≥ 0 and P_0 > 0:

- For all t, R_t ≥ 0 (by convex combination of non-negative terms).
- For all t, P_t > 0 and is non-increasing when loss_t ≥ 0.
- Effective time
  \[
  dt_\text{eff}(t) = \frac{1}{1 + R_t P_t}
  \]
  satisfies 0 < dt_eff(t) ≤ 1.

Code check: `tests/test_trp_state.py::test_trp_dt_eff_bounds`.
