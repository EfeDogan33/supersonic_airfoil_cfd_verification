import gmsh
import math


def mesh_generator(teta, chord):
    gmsh.initialize()

    rad = math.radians(teta)
    h_shoulder = (chord / 2) * math.tan(rad)


    p_le = gmsh.model.geo.addPoint(0, 0, 0)
    p_up = gmsh.model.geo.addPoint(chord / 2, h_shoulder, 0)
    p_te = gmsh.model.geo.addPoint(chord, 0, 0)
    p_down = gmsh.model.geo.addPoint(chord / 2, -h_shoulder, 0)

    line_up_front = gmsh.model.geo.addLine(p_le, p_up)
    line_up_back = gmsh.model.geo.addLine(p_up, p_te)
    line_down_front = gmsh.model.geo.addLine(p_le, p_down)
    line_down_back = gmsh.model.geo.addLine(p_down, p_te)

    p_front_top = gmsh.model.geo.addPoint(-2 * chord, 4 * chord, 0)
    p_front_top_le = gmsh.model.geo.addPoint(0, 4 * chord, 0)
    p_front_mid = gmsh.model.geo.addPoint(-2 * chord, 0, 0)
    p_front_down = gmsh.model.geo.addPoint(-2 * chord, -4 * chord, 0)
    p_front_down_le = gmsh.model.geo.addPoint(0, -4 * chord, 0)


    front_up_line1 = gmsh.model.geo.addLine(p_le, p_front_top_le)
    front_up_top_line = gmsh.model.geo.addLine(p_front_mid, p_front_top)
    front_mid_line = gmsh.model.geo.addLine(p_front_mid, p_le)
    front_top_boundary = gmsh.model.geo.addLine(p_front_top, p_front_top_le)

    cl_front_up = gmsh.model.geo.addCurveLoop([front_mid_line, front_up_line1, -front_top_boundary, -front_up_top_line])
    s_front_up = gmsh.model.geo.addPlaneSurface([cl_front_up])

    front_down_line1 = gmsh.model.geo.addLine(p_front_down, p_front_mid)
    front_down_line2 = gmsh.model.geo.addLine(p_front_down, p_front_down_le)
    front_down_line3 = gmsh.model.geo.addLine(p_front_down_le, p_le)

    cl_front_down = gmsh.model.geo.addCurveLoop([front_mid_line, -front_down_line3, -front_down_line2, front_down_line1])
    s_front_down = gmsh.model.geo.addPlaneSurface([cl_front_down])

    p_wedge_shoulder_up = gmsh.model.geo.addPoint(chord / 2, 4 * chord, 0)
    wedge_mid_to_up_line = gmsh.model.geo.addLine(p_up, p_wedge_shoulder_up)
    wedge_mid_top_line = gmsh.model.geo.addLine(p_front_top_le, p_wedge_shoulder_up)

    cl_wedge_front_up = gmsh.model.geo.addCurveLoop([line_up_front, wedge_mid_to_up_line, -wedge_mid_top_line, -front_up_line1])
    s_wedge_front_up = gmsh.model.geo.addPlaneSurface([cl_wedge_front_up])

    p_back_top_te = gmsh.model.geo.addPoint(chord, 4 * chord, 0)
    wedge_te_to_up_line = gmsh.model.geo.addLine(p_te, p_back_top_te)
    wedge_back_top_line = gmsh.model.geo.addLine(p_wedge_shoulder_up, p_back_top_te)

    cl_wedge_back_up = gmsh.model.geo.addCurveLoop([line_up_back, wedge_te_to_up_line, -wedge_back_top_line, -wedge_mid_to_up_line])
    s_wedge_back_up = gmsh.model.geo.addPlaneSurface([cl_wedge_back_up])

    p_wedge_shoulder_down = gmsh.model.geo.addPoint(chord / 2, -4 * chord, 0)
    p_back_down_te = gmsh.model.geo.addPoint(chord, -4 * chord, 0)

    wedge_front_down_line = gmsh.model.geo.addLine(p_front_down_le, p_wedge_shoulder_down)
    wedge_mid_to_down_line = gmsh.model.geo.addLine(p_wedge_shoulder_down, p_down)

    cl_wedge_front_down = gmsh.model.geo.addCurveLoop([line_down_front, -wedge_mid_to_down_line, -wedge_front_down_line, front_down_line3])
    s_wedge_front_down = gmsh.model.geo.addPlaneSurface([cl_wedge_front_down])

    wedge_back_down_line = gmsh.model.geo.addLine(p_wedge_shoulder_down, p_back_down_te)
    wedge_back_down_to_te_line = gmsh.model.geo.addLine(p_back_down_te, p_te)

    cl_wedge_back_down = gmsh.model.geo.addCurveLoop([line_down_back, -wedge_back_down_to_te_line, -wedge_back_down_line, wedge_mid_to_down_line])
    s_wedge_back_down = gmsh.model.geo.addPlaneSurface([cl_wedge_back_down])

    p_back_mid = gmsh.model.geo.addPoint(6 * chord, 0, 0)
    p_back_up_top = gmsh.model.geo.addPoint(6 * chord, 4 * chord, 0)
    p_back_down = gmsh.model.geo.addPoint(6 * chord, -4 * chord, 0)

    line_back_mid = gmsh.model.geo.addLine(p_te, p_back_mid)
    line_back_mid_to_top = gmsh.model.geo.addLine(p_back_mid, p_back_up_top)
    line_back_top = gmsh.model.geo.addLine(p_back_top_te, p_back_up_top)

    cl_back_up = gmsh.model.geo.addCurveLoop([line_back_mid, line_back_mid_to_top, -line_back_top, -wedge_te_to_up_line])
    s_back_up = gmsh.model.geo.addPlaneSurface([cl_back_up])

    line_back_down = gmsh.model.geo.addLine(p_back_down_te, p_back_down)
    line_back_down_to_mid = gmsh.model.geo.addLine(p_back_down, p_back_mid)

    cl_back_down = gmsh.model.geo.addCurveLoop([-wedge_back_down_to_te_line, line_back_down, line_back_down_to_mid, -line_back_mid])
    s_back_down = gmsh.model.geo.addPlaneSurface([cl_back_down])


    all_v_lines_up = [front_up_line1, front_up_top_line, wedge_mid_to_up_line, wedge_te_to_up_line, line_back_mid_to_top]
    all_v_lines_down = [front_down_line1, front_down_line3, wedge_mid_to_down_line, wedge_back_down_to_te_line, line_back_down_to_mid]

    n_wedge = 91
    n_far = 91
    ny = 121

    for line in all_v_lines_up:
        gmsh.model.geo.mesh.setTransfiniteCurve(line, ny, "Progression", 1.04)

    for line in all_v_lines_down:
        gmsh.model.geo.mesh.setTransfiniteCurve(line, ny, "Progression", -1.04)

    gmsh.model.geo.mesh.setTransfiniteCurve(line_up_front, n_wedge, "Bump", 0.03)
    gmsh.model.geo.mesh.setTransfiniteCurve(wedge_mid_top_line, n_wedge, "Bump", 0.03)
    gmsh.model.geo.mesh.setTransfiniteCurve(line_up_back, n_wedge, "Bump", 0.03)
    gmsh.model.geo.mesh.setTransfiniteCurve(wedge_back_top_line, n_wedge, "Bump", 0.03)
    gmsh.model.geo.mesh.setTransfiniteCurve(line_down_front, n_wedge, "Bump", 0.03)
    gmsh.model.geo.mesh.setTransfiniteCurve(wedge_front_down_line, n_wedge, "Bump", 0.03)
    gmsh.model.geo.mesh.setTransfiniteCurve(line_down_back, n_wedge, "Bump", 0.03)
    gmsh.model.geo.mesh.setTransfiniteCurve(wedge_back_down_line, n_wedge, "Bump", 0.03)

    gmsh.model.geo.mesh.setTransfiniteCurve(front_mid_line, n_far, "Progression", -1.03)
    gmsh.model.geo.mesh.setTransfiniteCurve(front_top_boundary, n_far, "Progression", -1.03)
    gmsh.model.geo.mesh.setTransfiniteCurve(front_down_line2, n_far, "Progression", -1.03)
    gmsh.model.geo.mesh.setTransfiniteCurve(line_back_mid, n_far, "Progression", 1.03)
    gmsh.model.geo.mesh.setTransfiniteCurve(line_back_top, n_far, "Progression", 1.03)
    gmsh.model.geo.mesh.setTransfiniteCurve(line_back_down, n_far, "Progression", 1.03)

    surfaces = [
        s_front_up, s_front_down,
        s_wedge_front_up, s_wedge_back_up,
        s_wedge_front_down, s_wedge_back_down,
        s_back_up, s_back_down
    ]

    for s in surfaces:
        gmsh.model.geo.mesh.setTransfiniteSurface(s)
        gmsh.model.geo.mesh.setRecombine(2, s)

    gmsh.model.geo.synchronize()


    airfoil_lines = [line_up_front, line_up_back, line_down_front, line_down_back]
    gmsh.model.addPhysicalGroup(1, airfoil_lines, name="airfoil")

    farfield_lines = [
        front_up_top_line, front_down_line1,
        front_top_boundary, wedge_mid_top_line, wedge_back_top_line, line_back_top,
        front_down_line2, wedge_front_down_line, wedge_back_down_line, line_back_down,
        line_back_mid_to_top, line_back_down_to_mid
    ]
    gmsh.model.addPhysicalGroup(1, farfield_lines, name="farfield")

    gmsh.model.addPhysicalGroup(2, surfaces, name="fluid")

    gmsh.option.setNumber("Mesh.Algorithm", 8)
    gmsh.model.mesh.generate(2)


    gmsh.write("double_wedge_su2/test_wedge.su2")
    gmsh.write("double_wedge_su2/test_wedge.vtk")
    gmsh.finalize()


