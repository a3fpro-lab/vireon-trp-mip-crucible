from dataclasses import dataclass

@dataclass
class VireonConfig:
    beta: float = 1.0
    eps_green: float = 1e-3
    eps_yellow: float = 5e-3
    alpha: float = 0.1
    eta_R: float = 0.05
    collapse_window: int = 200
    collapse_min_improvement: float = 1e-3
