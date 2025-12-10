from vireon_trp_mip.toy_solver import ToySearchProblem, run_baseline, run_vireon
from vireon_trp_mip.config import VireonConfig

def test_toy_baseline_runs():
    problem = ToySearchProblem(depth=5, noise=1.0, seed=1)
    stats = run_baseline(problem, max_nodes=1000)
    assert stats.nodes_expanded > 0
    assert stats.best_true_value < 1e6

def test_toy_vireon_runs():
    problem = ToySearchProblem(depth=5, noise=1.0, seed=1)
    cfg = VireonConfig()
    stats = run_vireon(problem, config=cfg, max_nodes=1000)
    assert stats.nodes_expanded > 0
    assert stats.best_true_value < 1e6
