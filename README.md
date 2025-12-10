# VIREON TRP MIP Crucible

**Status:** Experimental · Open · Falsifiable  
**Crucible target:** MIPLIB 2017 (design ready)  
**This repo:** Core TRP + KL-leash + collapse engine + toy crucible

This repo implements the core VIREON control stack:

- **TRP Law:** `T = R × P` with effective time dilation.
- **KL-Leash:** limits how far the search distribution moves per step.
- **Collapse Laws:** detect entropy-stagnant regions and kill them.

Today, the package includes:

- A fully working **toy search solver** that explores a synthetic search tree.
- Plug-in **TRP + KL-leash + collapse** controller that chooses nodes.
- Metrics and scripts to compare **baseline vs VIREON** on the toy problem.

The repo is also structured so you can extend it to real MIP solvers (SCIP / HiGHS)
and eventually run the **MIPLIB 2017 Crucible** (240-instance benchmark and
4 falsifiers).

This is meant for **serious evaluation** — the math is explicit, the algorithms are
clean, and all pieces are ready for public audit.

## Install (dev mode, on a laptop)

```bash
git clone https://github.com/<your-user>/vireon-trp-mip-crucible.git
cd vireon-trp-mip-crucible
pip install -e .[dev]
