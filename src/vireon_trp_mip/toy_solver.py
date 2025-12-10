from __future__ import annotations
from dataclasses import dataclass
import math
import random
from typing import Optional, List

from .controller import VireonNodeSelector
from .config import VireonConfig

@dataclass
class ToyNode:
    id: int
    depth: int
    true_value: float
    heuristic_score: float
    parent_id: Optional[int] = None

class ToySearchProblem:
    """
    Synthetic search problem:
    - Binary tree of fixed depth.
    - Leaves have "true_value".
    - Goal: find leaf with minimal true_value.
    - heuristic_score = true_value + noise.
    """
    def __init__(self, depth: int, noise: float, seed: int):
        self.depth = depth
        self.noise = noise
        self.rng = random.Random(seed)
        self.nodes: dict[int, ToyNode] = {}
        self.next_id = 0
        self.root_id = self._make_node(depth=0, parent_id=None)

    def _make_node(self, depth: int, parent_id: Optional[int]) -> int:
        node_id = self.next_id
        self.next_id += 1
        true_value = self.rng.gauss(0, 1.0)
        heuristic = true_value + self.rng.gauss(0, self.noise)
        self.nodes[node_id] = ToyNode(
            id=node_id,
            depth=depth,
            true_value=true_value,
            heuristic_score=heuristic,
            parent_id=parent_id,
        )
        return node_id

    def expand(self, node_id: int) -> List[int]:
        node = self.nodes[node_id]
        if node.depth >= self.depth:
            return []
        children = []
        for _ in range(2):
            cid = self._make_node(depth=node.depth + 1, parent_id=node_id)
            children.append(cid)
        return children

@dataclass
class SearchStats:
    nodes_expanded: int = 0
    best_true_value: float = math.inf

def run_baseline(problem: ToySearchProblem, max_nodes: int = 10000) -> SearchStats:
    open_list = [problem.root_id]
    stats = SearchStats()
    while open_list and stats.nodes_expanded < max_nodes:
        open_list.sort(key=lambda nid: problem.nodes[nid].heuristic_score)
        nid = open_list.pop(0)
        node = problem.nodes[nid]
        stats.nodes_expanded += 1
        stats.best_true_value = min(stats.best_true_value, node.true_value)
        children = problem.expand(nid)
        open_list.extend(children)
    return stats

def run_vireon(
    problem: ToySearchProblem,
    config: VireonConfig,
    max_nodes: int = 10000,
) -> SearchStats:
    open_list = [problem.root_id]
    selector = VireonNodeSelector(config=config)
    stats = SearchStats()
    best_bound = math.inf

    while open_list and stats.nodes_expanded < max_nodes:
        scores = [-problem.nodes[nid].heuristic_score for nid in open_list]
        idx, info = selector.select(scores, best_bound=best_bound)
        nid = open_list.pop(idx)
        node = problem.nodes[nid]
        stats.nodes_expanded += 1
        stats.best_true_value = min(stats.best_true_value, node.true_value)
        best_bound = stats.best_true_value
        children = problem.expand(nid)
        open_list.extend(children)

    return stats
