import numpy as np

def kl_div(p: np.ndarray, q: np.ndarray, eps: float = 1e-12) -> float:
    p = np.asarray(p, dtype=float)
    q = np.asarray(q, dtype=float)
    p = np.clip(p, eps, None)
    q = np.clip(q, eps, None)
    p /= p.sum()
    q /= q.sum()
    return float(np.sum(p * np.log(p / q)))

def apply_kl_leash(
    q_new: np.ndarray,
    q_ref: np.ndarray,
    eps_green: float,
    eps_yellow: float,
) -> tuple[np.ndarray, float, str]:
    delta = kl_div(q_new, q_ref)
    if delta <= eps_green:
        return q_new, delta, "green"

    if delta >= eps_yellow:
        lam = eps_green / delta
    else:
        lam = (eps_yellow - delta) / (eps_yellow - eps_green)

    lam = float(np.clip(lam, 0.0, 1.0))
    q_leashed = lam * q_new + (1.0 - lam) * q_ref
    q_leashed /= q_leashed.sum()
    regime = "yellow" if delta < eps_yellow else "red"
    return q_leashed, delta, regime
