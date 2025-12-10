from __future__ import annotations
from dataclasses import dataclass
import numpy as np

from .config import VireonConfig
from .trp_state import TRPState
from .distributions import softmax_from_scores
from .kl_leash import apply_kl_leash
from .collapse_laws import CollapseTracker

@dataclass
class VireonNodeSelector:
    config: VireonConfig = VireonConfig()
    trp: TRPState = TRPState()
    collapse: CollapseTracker = CollapseTracker()

    def select(self, scores: list[float], best_bound: float) -> tuple[int, dict]:
        q = softmax_from_scores(scores, beta=self.config.beta)

        if self.trp.q_ref is None:
            self.trp.update_q_ref(q)

        q_leashed, delta_kl, regime = apply_kl_leash(
            q_new=q,
            q_ref=self.trp.q_ref,
            eps_green=self.config.eps_green,
            eps_yellow=self.config.eps_yellow,
        )

        loss_t = 0.0
        self.trp.update_R(delta_kl)
        self.trp.update_P(loss_t)

        collapsed = self.collapse.update(best_bound)
        if collapsed:
            q_leashed = np.full_like(q_leashed, 1.0 / len(q_leashed))

        idx = int(np.argmax(q_leashed))
        self.trp.update_q_ref(q_leashed)
        self.trp.step += 1

        info = {
            "delta_kl": delta_kl,
            "regime": regime,
            "R": self.trp.R,
            "P": self.trp.P,
            "dt_eff": self.trp.dt_eff(),
            "collapsed": collapsed,
        }
        return idx, info
