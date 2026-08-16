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

## 2. Spatial Discretization & Numerical Schemes

To accurately capture sharp oblique shock discontinuities without non-physical numerical oscillations, a robust upwind scheme coupled with a slope limiter is utilized.

| Parameter | SU2 Setting | Description |
| :--- | :--- | :--- |
| **Convective Flux Scheme** | `HLLC` | Harten-Lax-van Leer-Contact exact Riemann solver, highly accurate for strong shocks. |
| **Spatial Order** | `MUSCL_FLOW= YES` | Second-order spatial accuracy for the convective fluxes using MUSCL reconstruction. |
| **Slope Limiter** | `VENKATAKRISHNAN` | Prevents overshoots near shock waves (Coefficient = 0.05) |
| **Gradient Calculation** | `GREEN_GAUSS` | Standard method for computing spatial gradients on the unstructured grid. |

---
## 3. Time Integration & Convergence Strategy

Steady-state convergence is achieved using an implicit time-stepping strategy with an adaptive Courant number to accelerate convergence once initial transients pass[cite: 1].

* **Time Stepping:** `EULER_IMPLICIT` 
* **Linear Solver:** `FGMRES` with `ILU` preconditioner (Error limit: $10^{-8}$, Max Iterations: 35)
* **CFL Strategy:** Adaptive CFL (`CFL_ADAPT= YES`) starting at `0.1` and ramping up to a maximum of `300.0`.

### 3.1 Convergence Criteria

The simulation is configured to run for a maximum of 4500 iterations, but will terminate early if the following strict criteria are met:

1. **Residual Drop:** The log-residual must drop by at least 5 orders of magnitude (`CONV_RESIDUAL_MINVAL= -5`).
2. **Cauchy Criteria (Force Stabilization):** The Drag coefficient must stabilize (`CONV_FIELD= DRAG`) within a tolerance of $10^{-6}$ (`CONV_CAUCHY_EPS= 1E-6`) over the last 100 iterations (`CONV_CAUCHY_ELEMS= 100`).

---

## 4. Boundary Marker Setup

The boundary markers defined during the mesh generation phase are explicitly mapped to SU2 boundary conditions:

```text
% ---------------- BOUNDARY CONDITIONS ----------------
MARKER_EULER= ( airfoil )
MARKER_FAR= ( farfield )


