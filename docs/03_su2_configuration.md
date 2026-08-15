# ⚙️ SU2 Configuration & Numerical Setup

This document details the configuration parameters and numerical methods applied in the **SU2** (Stanford University Unstructured) open-source CFD solver to compute the supersonic flow field and aerodynamic forces around the double-wedge airfoil.

---

## 1. Governing Equations & Flow Physics

Since the primary objective is to capture wave drag ($C_d$) induced by shock waves and expansion fans, the flow is modeled as **inviscid and compressible**. Boundary layer (viscous) effects are intentionally neglected to allow a direct comparison with the exact analytical 2D Shock-Expansion theory.

* **Governing Equations:** 2D Compressible Euler Equations (`SOLVER= EULER`)
* **Fluid Regime:** Supersonic (Ranging from $M_\infty = 2.0$ to $M_\infty = 4.0$ and $\alpha = 0.0^\circ$ to $\alpha = 15.0^\circ$)
* **Gas Model:** Ideal Gas (Air)
* **Specific Heat Ratio ($\gamma$):** $1.4$
* **Freestream Conditions:** $P_\infty = 101325.0 \text{ Pa}$, $T_\infty = 288.15 \text{ K}$

---
