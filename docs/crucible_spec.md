# MIPLIB 2017 Crucible Spec

Benchmark set: **MIPLIB 2017** (240 benchmark instances).

Baseline: any strong, publicly reproducible solver config that achieves:
- Solved ≈ 230–232 of 240 within standard time limit (e.g. 3600s)
- Geometric mean runtime ≤ 60 s on ≤ 16 threads

VIREON controller: TRP + KL-leash + collapse laws, integrated only at:
- Node selection / search control
- No new LP or cutting-plane tricks

## Metrics

For each instance and seed:

- `time_sec`: wall-clock time until status ∈ {optimal, time_limit, mem_limit}
- `nodes`: total branch-and-bound nodes
- `status`: optimal / time_limit / mem_limit / error
- `gap`: (best_primal - best_dual) / (1 + |best_primal|)
- `best_primal`, `best_dual`

Aggregate over all instances that baseline solves within time limit.

## Four falsifiers

Let `GM_time_base`, `GM_nodes_base` be geometric means for baseline,
and `GM_time_vir`, `GM_nodes_vir` for VIREON.

1. **≥100× node reduction**
   \[
   \frac{\text{GM\_nodes}_\text{vir}}{\text{GM\_nodes}_\text{base}} \le 0.01.
   \]

2. **≥10× runtime speedup**
   \[
   \frac{\text{GM\_time}_\text{vir}}{\text{GM\_time}_\text{base}} \le 0.1.
   \]

3. **Robustness floor**
   \[
   \text{Solved}_\text{vir} \ge \text{Solved}_\text{base} - 3.
   \]

4. **≥2× reduction in seed volatility**

   For each instance, compute ratio:
   \[
   r = \frac{\text{90th percentile time}}{\text{10th percentile time}}
   \]
   across ≥ 5 random seeds.

   Let `median_r_base`, `median_r_vir` be medians over the benchmark set.

   Requirement:
   \[
   \frac{\text{median\_r}_\text{vir}}{\text{median\_r}_\text{base}} \le 0.5.
   \]

## Protocol

- Use identical hardware for baseline and VIREON runs.
- Same solver version, same LP and cut settings.
- Only difference: node selection / search control (VIREON vs baseline).
- At least 5 seeds per instance.
- Publish:
  - solver version, flags, and configs
  - raw per-instance CSV
  - scripts to reproduce aggregates.
