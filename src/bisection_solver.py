import math


def bisection(func, a, b, tol=1e-6, max_iter=100):
    fa, fb = func(a), func(b)


    if abs(fa) < tol:
        return a
    if abs(fb) < tol:
        return b

    if fa * fb > 0:
        raise ValueError(f"This interval does not contain a root! f({a:.3f})={fa:.3f}, f({b:.3f})={fb:.3f}")

    for _ in range(max_iter):
        c = (a + b) / 2.0
        fc = func(c)
        if abs(fc) < tol or (b - a) / 2.0 < tol:
            return c

        if fc * fa < 0:
            b, fb = c, fc
        else:
            a, fa = c, fc
    return c


def prandtl_meyer(M, gamma=1.4):
    term1 = math.sqrt((gamma + 1) / (gamma - 1))
    term2 = math.atan(math.sqrt((gamma - 1) / (gamma + 1) * (M ** 2 - 1)))
    term3 = math.atan(math.sqrt(M ** 2 - 1))
    return term1 * term2 - term3


def solve_oblique_shock(M1, delta, gamma=1.4):
    if delta <= 1e-7:
        return None, M1, 1.0

    mu = math.asin(1.0 / M1)

    def theta_beta_m(beta):
        tan_delta = math.tan(delta)
        numerator = M1 ** 2 * math.sin(beta) ** 2 - 1
        denominator = M1 ** 2 * (gamma + math.cos(2 * beta)) + 2
        right_side = 2 * (1.0 / math.tan(beta)) * (numerator / denominator)
        return right_side - tan_delta

    beta_start = mu + 1e-5
    step = math.radians(0.05)
    b = beta_start + step
    found_positive = False

    while b < math.radians(75.0):
        if theta_beta_m(b) > 0:
            found_positive = True
            break
        b += step

    if not found_positive:
        raise ValueError(f"No weak shock solution found for M={M1} and delta={math.degrees(delta):.2f}°!")

    beta = bisection(theta_beta_m, beta_start, b)

    Mn1 = M1 * math.sin(beta)
    p2_p1 = 1 + (2 * gamma / (gamma + 1)) * (Mn1 ** 2 - 1)
    Mn2_sq = (1 + ((gamma - 1) / 2) * Mn1 ** 2) / (gamma * Mn1 ** 2 - (gamma - 1) / 2)
    M2 = math.sqrt(Mn2_sq) / math.sin(beta - delta)

    return beta, M2, p2_p1


def solve_expansion(M1, delta_theta, gamma=1.4):

    if abs(delta_theta) < 1e-7:
        return M1, 1.0

    nu1 = prandtl_meyer(M1, gamma)
    nu2_target = nu1 + delta_theta

    def pm_root(M):
        return prandtl_meyer(M, gamma) - nu2_target

    M2 = bisection(pm_root, M1, 20.0)
    p_ratio = ((1 + 0.5 * (gamma - 1) * M1 ** 2) / (1 + 0.5 * (gamma - 1) * M2 ** 2)) ** (gamma / (gamma - 1))

    return M2, p_ratio


def calc_double_wedge_cd(M_inf, half_wedge_angle_deg, chord, alpha_deg, gamma=1.4):
    alpha = math.radians(alpha_deg)
    theta = math.radians(half_wedge_angle_deg)


    delta1 = theta - alpha
    if delta1 > 1e-7:

        beta1, M1, p1_pinf = solve_oblique_shock(M_inf, delta1, gamma)
    elif abs(delta1) <= 1e-7:

        M1 = M_inf
        p1_pinf = 1.0
    else:

        M1, p1_pinf = solve_expansion(M_inf, abs(delta1), gamma)

    Cp1 = (p1_pinf - 1) / (0.5 * gamma * M_inf ** 2)


    delta2 = theta + alpha
    beta2, M2, p2_pinf = solve_oblique_shock(M_inf, delta2, gamma)
    Cp2 = (p2_pinf - 1) / (0.5 * gamma * M_inf ** 2)


    delta3 = 2 * theta
    M3, p3_p1 = solve_expansion(M1, delta3, gamma)
    p3_pinf = p3_p1 * p1_pinf
    Cp3 = (p3_pinf - 1) / (0.5 * gamma * M_inf ** 2)


    delta4 = 2 * theta
    M4, p4_p2 = solve_expansion(M2, delta4, gamma)
    p4_pinf = p4_p2 * p2_pinf
    Cp4 = (p4_pinf - 1) / (0.5 * gamma * M_inf ** 2)


    C_A = 0.5 * (Cp1 + Cp2 - Cp3 - Cp4) * math.tan(theta)
    C_N = 0.5 * (Cp2 - Cp1 + Cp4 - Cp3)

    Cd = C_A * math.cos(alpha) + C_N * math.sin(alpha)
    max_thickness = chord * math.tan(theta)

    return Cd

