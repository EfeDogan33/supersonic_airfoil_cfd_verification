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

## 2. Core Aerodynamic Solvers

### 2.1 Oblique Shock Wave Relation
For a given upstream Mach number ($M_1$) and deflection angle ($\delta$), the weak shock angle ($\beta$) is found by numerically solving the $\theta-\beta-\mathcal{M}$ relation using the **Bisection Method**:

$$\tan \theta = 2 \cot \beta \left[ \frac{M_1^2 \sin^2 \beta - 1}{M_1^2 (\gamma + \cos 2\beta) + 2} \right]$$

Once $\beta$ is converged, the normal Mach number is $M_{n1} = M_1 \sin \beta$. The static pressure ratio and downstream Mach number ($M_2$) are calculated as:

$$\frac{p_2}{p_1} = 1 + \frac{2\gamma}{\gamma + 1}(M_{n1}^2 - 1)$$

$$M_{n2}^2 = \frac{1 + \frac{\gamma - 1}{2} M_{n1}^2}{\gamma M_{n1}^2 - \frac{\gamma - 1}{2}}, \quad M_2 = \frac{M_{n2}}{\sin(\beta - \theta)}$$

### 2.2 Prandtl-Meyer Expansion Fan
For an expansion turning angle ($\Delta\theta$), the downstream Mach number is determined by evaluating the Prandtl-Meyer function $\nu(M)$:

$$\nu(M) = \sqrt{\frac{\gamma+1}{\gamma-1}} \arctan \sqrt{\frac{\gamma-1}{\gamma+1}(M^2-1)} - \arctan \sqrt{M^2-1}$$

The target downstream function is $\nu(M_2) = \nu(M_1) + \Delta\theta$. The solver uses the **Bisection Method** to inversely find $M_2$. The isentropic pressure ratio is then:

$$\frac{p_2}{p_1} = \left[ \frac{1 + \frac{\gamma-1}{2} M_1^2}{1 + \frac{\gamma-1}{2} M_2^2} \right]^{\frac{\gamma}{\gamma-1}}$$

---

## 3. Global Coefficient Integration

After determining the local static pressure ratios for all four faces ($p_1, p_2, p_3, p_4$ relative to $p_\infty$), the local pressure coefficients are evaluated:

$$C_{p,i} = \frac{\frac{p_i}{p_\infty} - 1}{0.5 \gamma M_\infty^2} \quad \text{for } i \in \{1, 2, 3, 4\}$$

By integrating these pressure coefficients over the projected geometry, the global **Axial Force Coefficient ($C_A$)** and **Normal Force Coefficient ($C_N$)** are obtained:

$$C_A = \frac{1}{2} (C_{p1} + C_{p2} - C_{p3} - C_{p4}) \tan(\theta)$$
$$C_N = \frac{1}{2} (C_{p2} - C_{p1} + C_{p4} - C_{p3})$$

Finally, the total **Wave Drag Coefficient ($C_d$)** is calculated by projecting $C_A$ and $C_N$ onto the freestream velocity vector (accounting for $\alpha$):

$$C_d = C_A \cos(\alpha) + C_N \sin(\alpha)$$

This pipeline strictly mirrors the logic in `src/bisection_solver.py`, ensuring exact analytical benchmarks across the entire operational envelope.
