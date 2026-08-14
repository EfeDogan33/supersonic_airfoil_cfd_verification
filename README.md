<div align="center">

#  Supersonic CFD Verification Pipeline (Double Wedge Airfoil)

> Verified supersonic CFD solution with **<0.25% error** and **<0.09% numerical uncertainty (GCI)**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![SU2](https://img.shields.io/badge/CFD-SU2%20Euler-orange)](https://su2code.github.io/)
[![Mesh](https://img.shields.io/badge/Mesh-Gmsh-green)](https://gmsh.info/)
[![Verification](https://img.shields.io/badge/Status-Verified-brightgreen)]()

<br>

<img src="./m4.0_a15.0_mach.png" width="95%">

<sub>Mach 4.0, α = 15° — Oblique shocks and expansion regions accurately captured</sub>

</div>

---
## ⚡ 30-Second Overview

This project presents an automated CFD verification pipeline for supersonic flow over a double wedge airfoil using Euler equations. Numerical results are verified against the analytical shock expansion theory, achieving high accuracy across different flight regimes and demonstrating excellent agreement between CFD and theory.

- 🎯 **<0.25% error** across 20 cases (Mach 2–4, AoA 0–15°)  
- 📐 **GCI-based uncertainty:** 0.087%  
- 📈 **Observed order:** p = 4.62  
- ✅ **Asymptotic convergence verified** (≈ 1.002)

- ---

## 📊 Key Results

### Drag Coefficient Verification

<div align="center">
  <img src="./cd_verification.png" width="88%">
</div>

| Mach | AoA Range | Max Error |
|:---:|:---:|:---:|
| **2.0** | 0°–15° | **< 0.19%** |
| **2.5** | 0°–15° | **< 0.17%** |
| **3.0** | 0°–15° | **< 0.20%** |
| **3.5** | 0°–15° | **< 0.23%** |
| **4.0** | 0°–15° | **< 0.24%** |

---

### Surface Pressure Validation (Cp)

<div align="center">
  <img src="./cp_distribution_final.png" width="88%">
</div>

- Shock regions captured without numerical smearing  
- Expansion discontinuity resolved sharply  
- Excellent agreement with analytical distribution  

---

##  Grid Convergence Index (GCI)

- **Observed order:** p = 4.62  
- **GCI (fine grid):** 0.087%  
- **Asymptotic ratio:** 1.002 → verified  

| Mesh | Elements | Cd |
|:---|:---:|:---:|
| **Fine** | 302K | 0.017720 |
| **Medium** | 167K | 0.017684 |
| **Coarse** | 86K | 0.017509 |

- **Richardson Extrapolated:** 0.017732  
- **Analytical Solution:** 0.017740 (Deviation: **0.043%**)  

---

## 🛠️ Pipeline Architecture

- Fully automated parametric study (20 cases)  
- Structured H-grid via Gmsh API for shock resolution
- Python-based post-processing (PyVista, Pandas, Matplotlib)  

---

# 📑 Technical Documentation

For in-depth mathematical derivations and solver configuration:
- 📐 [01. Mesh Generation & GCI Study](docs/01_mesh_generation_and_gci.md)
- 📖 [02. Analytical Shock-Expansion Theory](docs/02_analytical_theory.md)
- ⚙️ [03. SU2 Solver Configuration](docs/03_su2_configuration.md)
- 📊 [04. Post-Processing Pipeline](docs/04_postprocessing_pipeline.md)

---

---

## 🚀 Next Steps

- Adjoint-based drag optimization  
- Adaptive mesh refinement (AMR)  
- Extension to viscous (RANS) simulations  

---

## 👤 Author

**Efe Doğan**  
Aeronautical Engineering Undergraduate Student  
*Focus: CFD | High-Speed Aerodynamics | Numerical Methods*
