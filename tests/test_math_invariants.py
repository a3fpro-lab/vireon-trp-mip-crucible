import numpy as np

from vireon_trp_mip.kl_leash import kl_div, apply_kl_leash
from vireon_trp_mip.trp_state import TRPState
from vireon_trp_mip.collapse_laws import CollapseTracker


def test_kl_non_negative_and_zero_when_equal():
    p = np.array([0.3, 0.7])
    q = np.array([0.3, 0.7])
    d = kl_div(p, q)
    assert d >= 0.0
    assert abs(d) < 1e-12  # equal distributions ⇒ ≈ 0


def test_kl_positive_when_different():
    p = np.array([0.4, 0.6])
    q = np.array([0.3, 0.7])
    d = kl_div(p, q)
    assert d > 0.0


def test_kl_leash_reduces_divergence():
    q_ref = np.array([0.5, 0.5])
    q_new = np.array([0.9, 0.1])
    eps_green = 1e-3
    eps_yellow = 5e-3

    q_leashed, delta_orig, regime = apply_kl_leash(
        q_new, q_ref, eps_green, eps_yellow
    )

    d_orig = kl_div(q_new, q_ref)
    d_leashed = kl_div(q_leashed, q_ref)

    assert np.isclose(delta_orig, d_orig)  # delta is original KL
    assert d_leashed <= d_orig + 1e-9      # leash never increases KL
    assert d_leashed <= eps_yellow + 1e-3  # and is numerically small


def test_trp_dt_eff_bounds():
    trp = TRPState(R=0.5, P=2.0)
    dt = trp.dt_eff()
    assert dt > 0.0
    assert dt <= 1.0

    trp.R = 0.0
    trp.P = 1.0
    assert trp.dt_eff() == 1.0


def test_collapse_tracker_triggers_after_window():
    tracker = CollapseTracker(window=5, min_improvement=1e-3)
    bound = 0.0

    # first step initializes, no collapse
    assert tracker.update(bound) is False

    # no improvement, should collapse after 'window' steps
    collapsed = False
    for _ in range(10):
        collapsed = tracker.update(bound)
    assert collapsed is True
