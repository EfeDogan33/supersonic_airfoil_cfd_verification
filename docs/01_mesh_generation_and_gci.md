# Mesh Generation & Grid Convergence Index (GCI) Verification

## 1. Overview

This section presents the generation of structured H-grid meshes and the formal verification of spatial discretization errors using the ASME V&V 20 Grid Convergence Index (GCI) methodology. The objective is to demonstrate that the numerical solution lies within the asymptotic convergence range and is independent of grid resolution.

## 2. Domain & Boundary Conditions

A structured H-grid topology is employed to ensure alignment with shock waves and expansion fans, minimizing numerical dissipation and preserving discontinuities. The farfield boundaries are placed sufficiently far from the airfoil to eliminate boundary interference effects. Bump and progression parameters are applied in order to ensure that mesh is fine enough near the regions where shock waves and expansion fans are formed.

* **Airfoil:** Chord $c = 1.0\text{ m}$, thickness $t/c = 0.0875\%$ ($\theta =  5.0^\circ$)
* **Outer Boundaries (All):** `MARKER_FARFIELD`
* **Airfoil Surface:** `MARKER_EULER`

## 3. Mesh Visualizations

<div align="center">

** Fine Mesh (302k Cells) **
<img src="../fine_grid.png" width="95%">
* Figure 1: Structured H-grid used for the fine mesh. The fine mesh is selected as the primary mesh configuration throughout the pipeline, since it maintains a favorable balance between accuracy and computational costs.

** Medium Mesh (167k Cells) **
<img src="../medium_grid.png" width="95%">

** Coarse Mesh (86k Cells) **
<img src="../coarse_grid.png" width="95%">

## 4. Grid Convergence Study (GCI)

* Three-grid refinement analysis performed at $M_\infty = 2.0$, $\alpha = 0^\circ$:

| Grid | Elements | $C_d$ | Refinement Ratio ($r$) |
| :--- | :---: | :---: | :---: |
| **Fine (1)** | 302k | **0.017720** | — |
| **Medium (2)** | 167k | **0.017684** | $r_{21} = 1.342$ |
| **Coarse (3)** | 86k | **0.017509** | $r_{32} = 1.395$ |


