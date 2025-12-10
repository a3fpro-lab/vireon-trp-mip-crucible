from __future__ import annotations
from dataclasses import dataclass
import numpy as np

@dataclass
class TRPState:
    R: float = 0.0       # structural intensity
    P: float = 1.0       # policy momentum
    alpha: float = 0.1   # learning rate for P
    eta_R: float = 0.05  # smoothing for R
    q_ref: np.ndarray | None = None
    step: int = 0

    def dt_eff(self) -> float:
        """Effective subjective time increment: dt = 1/(1 + R*P)."""
        return 1.0 / (1.0 + self.R * self.P)

    def update_R(self, delta_kl: float) -> None:
        self.R = (1.0 - self.eta_R) * self.R + self.eta_R * float(delta_kl)

    def update_P(self, loss_t: float) -> None:
        self.P *= float(np.exp(-self.alpha * float(loss_t)))
        self.P = max(self.P, 1e-6)

    def update_q_ref(self, q: np.ndarray) -> None:
        self.q_ref = np.asarray(q, dtype=float).copy()
