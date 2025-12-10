# VIREON TRP Foundations

## 1. State and Time

At decision step t, with action set A_t and probability distribution q_t over A_t:

- Structural intensity: R_t ≥ 0
- Policy momentum: P_t > 0
- Effective time:
  \[
  dt_\text{eff}(t) = \frac{1}{1 + R_t P_t}.
  \]
This ensures:
\[
0 < dt_\text{eff}(t) \le 1.
\]

## 2. Scores → Distribution

Scores s_t(a) ∈ ℝ for a ∈ A_t, inverse temperature β_t > 0:

\[
q_t(a) = \frac{\exp(\beta_t s_t(a))}{\sum_{a' \in A_t} \exp(\beta_t s_t(a'))}.
\]

This defines a valid probability distribution:
\[
q_t(a) \ge 0,\quad \sum_a q_t(a) = 1.
\]

## 3. KL Divergence

For distributions p, q over the same finite set:

\[
D_\text{KL}(p \parallel q) = \sum_a p(a) \log\frac{p(a)}{q(a)}.
\]

Properties used in this repo:

1. **Non-negativity:**
   \[
   D_\text{KL}(p \parallel q) \ge 0.
   \]
2. **Zero iff equal (almost everywhere):**
   \[
   D_\text{KL}(p \parallel q) = 0 \iff p = q.
   \]
3. **Convexity in the first argument:**

   For 0 ≤ λ ≤ 1 and distributions p₁, p₂, q:

   \[
   D_\text{KL}(\lambda p_1 + (1-\lambda)p_2 \parallel q)
   \le
   \lambda D_\text{KL}(p_1 \parallel q) + (1-\lambda)D_\text{KL}(p_2 \parallel q).
   \]

## 4. KL-Leash

Let q_ref be a reference distribution and q_new the new proposal.
Define:
\[
\Delta = D_\text{KL}(q_\text{new} \parallel q_\text{ref}).
\]

Thresholds:
\[
0 < \varepsilon_\text{green} < \varepsilon_\text{yellow}.
\]

Define λ(Δ) by:
\[
\lambda(\Delta) =
\begin{cases}
1, & \Delta \le \varepsilon_\text{green},\\[4pt]
\dfrac{\varepsilon_\text{yellow}-\Delta}{\varepsilon_\text{yellow}-\varepsilon_\text{green}}, & \varepsilon_\text{green} < \Delta < \varepsilon_\text{yellow},\\[8pt]
\dfrac{\varepsilon_\text{green}}{\Delta}, & \Delta \ge \varepsilon_\text{yellow}.
\end{cases}
\]

The leashed distribution:
\[
q^\text{leash} = \lambda(\Delta)\,q_\text{new} + \bigl(1-\lambda(\Delta)\bigr)\,q_\text{ref}.
\]

By convexity:

\[
D_\text{KL}(q^\text{leash} \parallel q_\text{ref})
\le
\lambda(\Delta) D_\text{KL}(q_\text{new} \parallel q_\text{ref})
=
\lambda(\Delta)\,\Delta.
\]

For the red regime (Δ ≥ ε_yellow):

\[
\lambda(\Delta)\,\Delta = \varepsilon_\text{green},
\]
so:
\[
D_\text{KL}(q^\text{leash} \parallel q_\text{ref}) \le \varepsilon_\text{green}.
\]

Thus the leash strictly bounds the post-leash divergence in the red regime.

## 5. TRP Updates

Let Δ_t = D_\text{KL}(q_t \parallel q_t^\text{ref}) at step t and loss_t ≥ 0.

Structural intensity update:
\[
R_{t+1} = (1-\eta_R) R_t + \eta_R\,\Delta_t,\quad 0 < \eta_R \le 1.
\]

Policy momentum update:
\[
P_{t+1} = P_t \exp(-\alpha\,\text{loss}_t),\quad \alpha > 0.
\]

From these definitions:

- R_t ≥ 0 for all t if R_0 ≥ 0 and Δ_t ≥ 0.
- P_t is monotonically non-increasing if loss_t ≥ 0.

## 6. Collapse Tracker

Best bound B_t (we assume minimization). A collapse is triggered if:

- Over a sliding window of W steps, there is no improvement larger than δ_min:
  \[
  B_t + \delta_\text{min} < B_{t'} \quad \text{never holds for any } t' > t-W,
  \]
  and
- The window length is reached.

This encodes a mathematical rule: any region with no qualifying improvement in W steps is identified as stagnating and can be pruned or reweighted.
