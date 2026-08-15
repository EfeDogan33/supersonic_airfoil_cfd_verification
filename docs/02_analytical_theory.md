# 🧮 Analytical Theory & Shock-Expansion Method

This document outlines the **2D Shock-Expansion Theory** implemented in the analytical solver to compute the exact aerodynamic coefficients (Axial Force $C_A$, Normal Force $C_N$, and Wave Drag $C_d$) for a symmetric double-wedge airfoil. The algorithm accounts for the freestream Mach number ($M_\infty$), half-wedge angle ($\theta$), and angle of attack ($\alpha$).

---

## 1. Flow Field Discretization (4-Face Model)

To accurately resolve the forces including the effects of the angle of attack ($\alpha$), the airfoil is divided into four distinct faces. The local deflection angle ($\delta$) for each face determines whether the flow undergoes compression (Oblique Shock) or expansion (Prandtl-Meyer fan).

1. **Face 1 (Upper Front):** $\delta_1 = \theta - \alpha$. If $\delta_1 > 0$, an oblique shock forms. If $\delta_1 < 0$, an expansion fan occurs.
2. **Face 2 (Lower Front):** $\delta_2 = \theta + \alpha$. An oblique shock wave compresses the flow.
3. **Face 3 (Upper Rear):** The flow from Face 1 expands over the shoulder by $\delta_3 = 2\theta$.
4. **Face 4 (Lower Rear):** The flow from Face 2 expands over the shoulder by $\delta_4 = 2\theta$.

---
