import math
import statistics
import csv
from pathlib import Path

from vireon_trp_mip.toy_solver import ToySearchProblem, run_baseline, run_vireon
from vireon_trp_mip.config import VireonConfig
from vireon_trp_mip.logging_utils import print_header


def geo_mean(xs):
    xs = [x for x in xs if x > 0]
    if not xs:
        return float("nan")
    logs = [math.log(x) for x in xs]
    return math.exp(sum(logs) / len(logs))


def main():
    print_header("Toy Stats: Baseline vs VIREON")

    out_path = Path("results/toy_stats.csv")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    seeds = range(1, 201)  # 200 runs each

    cfg = VireonConfig(
        beta=1.0,
        eps_green=1e-3,
        eps_yellow=5e-3,
        alpha=0.05,
        eta_R=0.05,
        collapse_window=200,
        collapse_min_improvement=1e-3,
    )

    rows = []

    base_nodes = []
    vir_nodes = []
    base_vals = []
    vir_vals = []

    for s in seeds:
        problem_b = ToySearchProblem(depth=10, noise=1.0, seed=s)
        stats_b = run_baseline(problem_b, max_nodes=10000)

        problem_v = ToySearchProblem(depth=10, noise=1.0, seed=s)
        stats_v = run_vireon(problem_v, config=cfg, max_nodes=10000)

        base_nodes.append(stats_b.nodes_expanded)
        vir_nodes.append(stats_v.nodes_expanded)
        base_vals.append(stats_b.best_true_value)
        vir_vals.append(stats_v.best_true_value)

        rows.append(
            {
                "seed": s,
                "baseline_nodes": stats_b.nodes_expanded,
                "vireon_nodes": stats_v.nodes_expanded,
                "baseline_best_value": stats_b.best_true_value,
                "vireon_best_value": stats_v.best_true_value,
            }
        )

    with out_path.open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "seed",
                "baseline_nodes",
                "vireon_nodes",
                "baseline_best_value",
                "vireon_best_value",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    print("Results written to", out_path)

    print()
    print("Node counts:")
    print(f"  baseline mean:   {statistics.mean(base_nodes):.2f}")
    print(f"  vireon   mean:   {statistics.mean(vir_nodes):.2f}")
    print(f"  baseline median: {statistics.median(base_nodes):.2f}")
    print(f"  vireon   median: {statistics.median(vir_nodes):.2f}")
    print(f"  baseline gmean:  {geo_mean(base_nodes):.2f}")
    print(f"  vireon   gmean:  {geo_mean(vir_nodes):.2f}")

    print()
    print("Best values (lower is better):")
    print(f"  baseline mean:   {statistics.mean(base_vals):.4f}")
    print(f"  vireon   mean:   {statistics.mean(vir_vals):.4f}")


if __name__ == "__main__":
    main()
