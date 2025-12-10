import numpy as np

from vireon_trp_mip.kl_leash import kl_div, apply_kl_leash

def main():
    q_ref = np.array([0.5, 0.5])
    q_new = np.array([0.9, 0.1])

    print("q_ref:", q_ref)
    print("q_new:", q_new)

    d_orig = kl_div(q_new, q_ref)
    print(f"Original KL(q_new || q_ref) = {d_orig:.6f}")

    q_leashed, delta_orig, regime = apply_kl_leash(
        q_new, q_ref, eps_green=1e-3, eps_yellow=5e-3
    )
    d_leashed = kl_div(q_leashed, q_ref)

    print("q_leashed:", q_leashed)
    print(f"Delta returned (orig KL) = {delta_orig:.6f}")
    print(f"KL(q_leashed || q_ref)   = {d_leashed:.6f}")
    print(f"Regime: {regime}")
    print(f"KL reduction factor: {d_leashed / d_orig:.3f}")

if __name__ == "__main__":
    main()
