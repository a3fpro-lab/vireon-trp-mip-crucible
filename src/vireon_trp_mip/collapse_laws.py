from dataclasses import dataclass

@dataclass
class CollapseTracker:
    window: int = 200
    min_improvement: float = 1e-3

    last_bound: float | None = None
    no_improve_count: int = 0

    def update(self, current_bound: float) -> bool:
        """Return True if collapse is triggered."""
        if self.last_bound is None:
            self.last_bound = float(current_bound)
            self.no_improve_count = 0
            return False

        # Assume minimization; improvement = lower bound
        if current_bound + self.min_improvement < self.last_bound:
            self.last_bound = float(current_bound)
            self.no_improve_count = 0
            return False

        self.no_improve_count += 1
        if self.no_improve_count >= self.window:
            self.no_improve_count = 0
            return True

        return False
