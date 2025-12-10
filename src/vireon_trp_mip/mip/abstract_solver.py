from abc import ABC, abstractmethod
from pathlib import Path
from dataclasses import dataclass

@dataclass
class SolverRunResult:
    instance: str
    seed: int
    status: str
    time_sec: float
    nodes: int
    gap: float | None
    best_primal: float | None
    best_dual: float | None

class AbstractMIPSolver(ABC):
    """Interface for plugging the Vireon controller into real solvers."""

    @abstractmethod
    def solve_instance(self, path: Path, seed: int) -> SolverRunResult:
        ...
