# VIREON TRP + KL-Leash + Collapse Laws (Math Spec)

## TRP Law

At decision step t, with action set A_t and distribution q_t(a):

- Structural intensity: R_t ≥ 0
- Policy momentum: P_t > 0
- TRP law: T = R × P

Effective subjective time increment:
\[
dt_\text{eff}(t) = \frac{1}{1 + R_t P_t}.
\]

## Scores → Distribution

Solver scores s_t(a) mapped via softmax:
\[
q_t(a) = \frac{\exp(\beta_t s_t(a))}{\sum_{a'} \exp(\beta_t s_t(a'))}.
\]

## KL-Leash

Reference distribution q_t^{ref}. Stepwise shift:
\[
\Delta_\text{KL}(t) = \sum_a q_t(a)\log\frac{q_t(a)}{q_t^{ref}(a)}.
\]

Thresholds:
\[
0 < \varepsilon_\text{green} < \varepsilon_\text{yellow}.
\]

Leashed distribution:
\[
q_t^\text{leash} = \lambda_t q_t + (1-\lambda_t) q_t^{ref}.
\]

Where
\[
\lambda_t =
\begin{cases}
1, & \Delta_\text{KL}\le\varepsilon_\text{green},\\
\frac{\varepsilon_\text{yellow}-\Delta_\text{KL}}{\varepsilon_\text{yellow}-\varepsilon_\text{green}},
& \varepsilon_\text{green}<\Delta_\text{KL}<\varepsilon_\text{yellow},\\
\frac{\varepsilon_\text{green}}{\Delta_\text{KL}},
& \Delta_\text{KL}\ge\varepsilon_\text{yellow}.
\end{cases}
\]

## TRP Updates

\[
R_{t+1} = (1-\eta_R) R_t + \eta_R \Delta_\text{KL}(t),
\]
\[
P_{t+1} = P_t \exp(-\alpha\,\text{loss}_t).
\]

## Collapse Law

Track best bound B_t. Collapse if for some window:

- No improvement >= min_improvement
- Nodes spent in that region exceed window

In code: `CollapseTracker.update(current_bound)` returns True to trigger pruning
or reweighting of that subtree.

## Node Selection

1. Scores → q_t via softmax.
2. KL-leash → q_t^\text{leash}.
3. Update R_t, P_t.
4. Check collapse.
5. Choose argmax of q_t^\text{leash}.
