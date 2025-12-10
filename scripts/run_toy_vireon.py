import statistics
from vireon_trp_mip.toy_solver import ToySearchProblem, run_vireon
from vireon_trp_mip.config import VireonConfig
from vireon_trp_mip.logging_utils import print_header

def main():
    print_header("Toy VIREON")
    seeds = range(1, 21)
    nodes_list = []
    bestvals = []
    config = VireonConfig(
        beta=1.0,
        eps_green=1e-3,
        eps_yellow=5e-3,
        alpha=0.05,
        eta_R=0.05,
        collapse_window=200,
        collapse_min_improvement=1e-3,
    )
    for s in seeds:
        problem = ToySearchProblem(depth=10, noise=1.0, seed=s)
        stats = run_vireon(problem, config=config)
        nodes_list.append(stats.nodes_expanded)
        bestvals.append(stats.best_true_value)
    print(f"Runs: {len(seeds)}")
    print(f"Avg nodes expanded: {statistics.mean(nodes_list):.1f}")
    print(f"Median nodes expanded: {statistics.median(nodes_list):.1f}")
    print(f"Avg best true value: {statistics.mean(bestvals):.3f}")

if __name__ == "__main__":
    main()
