from pathlib import Path
import numpy as np
import pandas as pd
import pyvista as pv


def generate_all_contours(vtu_path: Path, output_dir: Path, prefix: str, freestream_mach: float = None):

    if not vtu_path.exists():
        print(f"   [PostProcess Warning] VTU file can't be found: {vtu_path.name}")
        return

    try:
        mesh = pv.read(vtu_path)


        press_col = next((c for c in mesh.array_names if 'PRESSURE' in c.upper()), None)
        mach_col = next((c for c in mesh.array_names if 'MACH' in c.upper()), None)

        if press_col:

            p_inf = float(np.median(mesh[press_col]))


            if freestream_mach is not None:
                m_inf = freestream_mach
            elif mach_col:
                m_inf = float(np.median(mesh[mach_col]))
            else:
                m_inf = 2.0


            gamma = 1.4
            q_inf = 0.5 * gamma * p_inf * (m_inf ** 2)


            mesh["Cp"] = (mesh[press_col] - p_inf) / q_inf


        fields_to_plot = []

        if mach_col:
            fields_to_plot.append(("Mach", "Mach Number", "turbo", False, True, 4.0))

        if "Cp" in mesh.array_names:
            fields_to_plot.append(("Cp", "Pressure Coefficient (Cp)", "coolwarm", False, True, 4.0))


        density_col = next((c for c in mesh.array_names if 'DENSITY' in c.upper()), None)
        if density_col:
            mesh_with_grad = mesh.compute_derivative(scalars=density_col, gradient="Density_Gradient")
            grad_vectors = mesh_with_grad["Density_Gradient"]


            grad_mag = np.sqrt(grad_vectors[:, 0] ** 2 + grad_vectors[:, 1] ** 2 + grad_vectors[:, 2] ** 2)


            mesh["Schlieren"] = np.sqrt(grad_mag)


            fields_to_plot.append(("Schlieren", "Numerical Schlieren (|∇ρ|)", "bone", False, False, 4.0))


        for field_name, title_label, cmap_choice, log_scale, show_bar, zoom_level in fields_to_plot:
            img_path = output_dir / f"{prefix}_{field_name.lower()}.png"
            plotter = pv.Plotter(off_screen=True)


            if field_name == "Schlieren":
                plotter.background_color = 'black'
            else:
                plotter.background_color = 'white'


            clim_val = None

            if field_name == "Schlieren":

                p_high = np.percentile(mesh["Schlieren"], 98.5)
                clim_val = [0.0, p_high]

            elif field_name == "Mach":

                p_low = np.percentile(mesh["Mach"], 3.0)
                p_high = np.max(mesh["Mach"])
                clim_val = [p_low, p_high]

            elif field_name == "Cp":

                cp_abs_max = np.percentile(np.abs(mesh["Cp"]), 98.5)
                clim_val = [-cp_abs_max, cp_abs_max]

            plotter.add_mesh(
                mesh,
                scalars=field_name,
                cmap=cmap_choice,
                show_edges=False,
                smooth_shading=True,
                log_scale=log_scale,
                clim=clim_val,
                show_scalar_bar=show_bar,
                scalar_bar_args={
                    "title": title_label,
                    "color": "black",
                    "title_font_size": 45,
                    "label_font_size": 32,
                    "vertical": False,
                    "position_x": 0.25,
                    "position_y": 0.05,
                    "width": 0.5
                } if show_bar else None
            )

            plotter.view_xy()
            plotter.enable_parallel_projection()
            plotter.reset_camera()
            plotter.camera.zoom(zoom_level)

            plotter.screenshot(img_path, window_size=[3840, 2160])


            plotter.deep_clean()
            plotter.close()
            print(f"   --> 4K {field_name} image is saved: {img_path.name}")

    except Exception as e:
        print(f"   [PostProcess Error] PyVista error: {e}")


def parse_history_data(work_dir: Path, history_prefix: str) -> tuple[float, float] | None:

    possible_files = [
        work_dir / f"{history_prefix}.csv",
        work_dir / f"{history_prefix}.dat",
        work_dir / "history.csv",
        work_dir / "history.dat"
    ]

    found_file = next((f for f in possible_files if f.exists()), None)
    if not found_file:
        return None

    try:
        try:
            df = pd.read_csv(found_file, skipinitialspace=True)
        except Exception:
            df = pd.read_csv(found_file, sep=r'\s+|,', engine='python')

        df.columns = [str(c).replace('"', '').replace("'", "").strip() for c in df.columns]

        cd_col = next((c for c in df.columns if 'CD' in c.upper()), None)
        cl_col = next((c for c in df.columns if 'CL' in c.upper()), None)

        if cd_col and cl_col:
            last_cl = float(df[cl_col].dropna().iloc[-1])
            last_cd = float(df[cd_col].dropna().iloc[-1])
            return last_cl, last_cd
        return None
    except Exception:
        return None


def export_to_excel(results: list, output_path: Path):

    if not results:
        return

    df_results = pd.DataFrame(results)

    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        df_results.to_excel(writer, sheet_name='Results', index=False)
        worksheet = writer.sheets['Results']


        for col in worksheet.columns:
            max_len = max(len(str(cell.value or '')) for cell in col)
            col_letter = col[0].column_letter
            worksheet.column_dimensions[col_letter].width = max(max_len + 3, 12)

    print(f"\n[Report OK] Excel file is saved : {output_path}")
