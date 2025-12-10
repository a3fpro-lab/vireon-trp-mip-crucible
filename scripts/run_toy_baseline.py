import statistics
from vireon_trp_mip.toy_solver import ToySearchProblem, run_baseline
from vireon_trp_mip.logging_utils import print_header

def main():
    print_header("Toy Baseline")
    seeds = range(1, 21)
    nodes_list = []
    bestvals = []
    for s in seeds:
        problem = ToySearchProblem(depth=10, noise=1.0, seed=s)
        stats = run_baseline(problem)
        nodes_list.append(stats.nodes_expanded)
        bestvals.append(stats.best_true_value)
    print(f"Runs: {len(seeds)}")
    print(f"Avg nodes expanded: {statistics.mean(nodes_list):.1f}")
    print(f"Median nodes expanded: {statistics.median(nodes_list):.1f}")
    print(f"Avg best true value: {statistics.mean(bestvals):.3f}")

if __name__ == "__main__":
    main()
