# API Overview

## Core components

- `TRPState` (`trp_state.py`): holds R, P, q_ref and updates them.
- `softmax_from_scores` (`distributions.py`): maps scores → probabilities.
- `apply_kl_leash` (`kl_leash.py`): constrains distribution shifts by KL.
- `CollapseTracker` (`collapse_laws.py`): detects stagnation and triggers collapse.
- `VireonNodeSelector` (`controller.py`): combines all of the above into a policy.
- `ToySearchProblem` and runners (`toy_solver.py`): toy tree search environment.

## Typical flow

1. Environment or solver emits candidate actions with scores.
2. Scores → `softmax_from_scores` → q_t.
3. `apply_kl_leash(q_t, q_ref, eps_green, eps_yellow)` → q_t^leash.
4. `TRPState` updated with ΔKL and loss.
5. `CollapseTracker.update(best_bound)` decides if region collapses.
6. `VireonNodeSelector.select(scores, best_bound)` returns chosen index and diagnostics.
