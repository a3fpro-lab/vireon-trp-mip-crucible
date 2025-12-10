from vireon_trp_mip.trp_state import TRPState

def test_trp_updates():
    trp = TRPState()
    trp.update_R(0.1)
    trp.update_P(loss_t=1.0)
    assert trp.R > 0
    assert trp.P < 1.0
    assert trp.dt_eff() > 0
