from pathlib import Path
import subprocess
import shutil

def create_run_config(base_cfg: Path, target_cfg: Path, mach: float, AoA: float, history_prefix: str, mesh_name: str):
    base_cfg = base_cfg.resolve()
    target_cfg = target_cfg.resolve()

    if not base_cfg.exists():
        print(f"   [SU2 Runner Error] Main CFG file cannot be found!: {base_cfg}")
        return

    with open(base_cfg, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("MACH_NUMBER="):
            new_lines.append(f"MACH_NUMBER= {mach}\n")
        elif stripped.startswith("AOA="):
            new_lines.append(f"AOA= {AoA}\n")
        elif stripped.startswith("CONV_FILENAME="):
            new_lines.append(f"CONV_FILENAME= {history_prefix}\n")
        elif stripped.startswith("MESH_FILENAME="):
            new_lines.append(f"MESH_FILENAME= ../{mesh_name}\n")
        else:
            new_lines.append(line)

    with open(target_cfg, "w", encoding="utf-8") as f:
        f.writelines(new_lines)


def run_simulation(work_dir: Path, target_cfg_name: str, num_process: int = 4) -> bool:
    abs_work_dir = work_dir.resolve()
    target_cfg_path = (abs_work_dir / target_cfg_name).resolve()

    if not target_cfg_path.exists():
        print(f"   [SU2 Runner Error] Config file cannot be found!: {target_cfg_path}")
        return False


    su2_executable = shutil.which("SU2_CFD")


    if su2_executable is None:
        print("   !! [SU2 Runner Error] 'SU2_CFD' was not found in the system PATH variables.")
        print("   Please add the directory where SU2 is installed to your environment variables.")
        return False

    try:

        subprocess.run(
            ["mpiexec", "-n", str(num_process), su2_executable, str(target_cfg_path)],
            cwd=str(abs_work_dir),
            check=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"   !! [SU2 Runner Error] Simulation stopped (Exit Code: {e.returncode})")
        return False
    except Exception as e:
        print(f"   !! [SU2 Runner Error] Unexpected system error: {e}")
        return False
