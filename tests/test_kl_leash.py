import numpy as np
from vireon_trp_mip.kl_leash import apply_kl_leash

def test_kl_leash_green_zone():
    q_ref = np.array([0.5, 0.5])
    q_new = np.array([0.51, 0.49])
    q_leashed, delta, regime = apply_kl_leash(
        q_new, q_ref, eps_green=1e-2, eps_yellow=5e-2
    )
    assert regime == "green"
    assert np.isclose(q_leashed.sum(), 1.0)
    assert delta >= 0.0
