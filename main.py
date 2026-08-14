from pathlib import Path
import mesh_generator
from su2_runner import create_run_config, run_simulation
import bisection_solver as bs
import postprocess as pp


BASE_DIR = Path(__file__).resolve().parent
SU2_DIR = BASE_DIR / "double_wedge_su2"
BASE_CFG_PATH = SU2_DIR / "double_wedge.cfg"
MESH_NAME = "test_wedge.su2"
MESH_PATH = SU2_DIR / MESH_NAME

MACH_NUMBERS = [2.0]
AOA_VALUES = [0.0]
NUM_PROCESS = 4
CHORD_LENGTH  = 1.0

HALF_WEDGE_ANGLE = 5.0

def main():

    if not MESH_PATH.exists():
        print(f"[Mesh Status] {MESH_NAME} can't be found!")
        mesh_generator(teta=HALF_WEDGE_ANGLE, chord=CHORD_LENGTH, output_path=MESH_PATH)
    else:
        print(f"[Mesh Status] {MESH_NAME} confirmed.")

    results = []
    run_count = 1
    total_runs = len(MACH_NUMBERS) * len(AOA_VALUES)


    for mach in MACH_NUMBERS:
        for aoa in AOA_VALUES:
            print(f"\n[{run_count}/{total_runs}] Analysis is initialized! -> Mach: {mach} | AoA: {aoa}")

            work_dir = SU2_DIR / f"run_m{mach}_a{aoa}"
            work_dir.mkdir(parents=True, exist_ok=True)

            target_cfg_name = f"config_m{mach}_a{aoa}.cfg"
            target_cfg_path = work_dir / target_cfg_name
            history_prefix = f"history_m{mach}_a{aoa}"


            create_run_config(BASE_CFG_PATH, target_cfg_path, mach, aoa, history_prefix, MESH_NAME)
            success = run_simulation(work_dir, target_cfg_name, num_process=NUM_PROCESS)

            if success:

                default_vtu = work_dir / "flow.vtu"
                custom_vtu = work_dir / f"flow_m{mach}_a{aoa}.vtu"
                if default_vtu.exists():
                    default_vtu.rename(custom_vtu)


                pp.generate_all_contours(custom_vtu, work_dir, prefix=f"m{mach}_a{aoa}",freestream_mach=mach)


                parsed_data = pp.parse_history_data(work_dir, history_prefix)
                if parsed_data:
                    last_cl, last_cd = parsed_data

                    analytical_cd = bs.calc_double_wedge_cd(
                        M_inf=mach,
                        half_wedge_angle_deg=HALF_WEDGE_ANGLE,
                        chord=CHORD_LENGTH,
                        alpha_deg=aoa
                    )

                    error_pct = (abs(last_cd - analytical_cd) / abs(analytical_cd)) * 100

                    results.append({
                        "Mach": mach,
                        "AoA (deg)": aoa,
                        "Cl (SU2)": round(last_cl, 6),
                        "Cd (SU2)": round(last_cd, 6),
                        "Cd (Analytical)": round(analytical_cd, 6),
                        "Error (%)": round(error_pct, 3)
                    })
                    print(f"   --> Verification is completed: Error = %{round(error_pct, 2)}")

            run_count += 1


    excel_path = BASE_DIR / "Mach_AoA_Cd_Comparison.xlsx"
    pp.export_to_excel(results, excel_path)

if __name__ == "__main__":
    main()
