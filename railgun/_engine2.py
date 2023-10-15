"""
e2 engine

Second version of engine for calculating math model of
flight object in the field of gravity and air resistance
"""

import numpy as np
import numpy.random as rnd
import matplotlib.pyplot as plt
from scipy.integrate import ode


def __func2(t, y, k: float):
    """
        The function of the right-hand sides of the ODE system with the condition
    that the resistance force of a moving projectile is proportional to the square
    of its velocity with a coefficient k.
    (has an additional argument k)

    :param t: scipy.integrate.ode default argument, define as time, [s]
    :param y: integration variable
    :param k: drag coefficient, aerodynamic_coefficient / weight
    :return: [float, float, float, float]
    """
    G = 9.81
    y1, y2, y3, y4 = y

    return [
        y2,
        -k * y2 * np.sqrt(y2 ** 2 + y4 ** 2),
        y4,
        -k * y4 * np.sqrt(y2 ** 2 + y4 ** 2) - G
    ]


def __func3(t, y, k: float):
    """
        The function of the right-hand sides of the ODE system with the condition
    that the resistance force of a moving projectile is proportional to the cube
    of its velocity with a coefficient k.
    (has an additional argument k)

    :param t: scipy.integrate.ode default argument, define as time, [s]
    :param y: integration variable
    :param k: drag coefficient, aerodynamic_coefficient / weight
    :return: [float, float, float, float]
    """
    G = 9.81
    y1, y2, y3, y4 = y

    return [
        y2,                 # y1' = y2
        -k * y2**3,         # y2' = -k * y2**3
        y4,                 # y3' = y4
        -k * y4**3 - G      # y4' = -k * y4**3 - g
    ]


class ODESolution:
    """
        Transport class
        Contains necessary value for further operation after solving system of ODE
    """
    IntegrlVars = []
    TimeLine = []
    FlightTime = 0
    Distance = 0
    Height = 0

    x_shell = 0
    y_shell = 0

def _calc_setup(railgun):
    """
        Setup value for further calculating
    :return: ODESolution
    """
    alpha = railgun.alpha
    beta = railgun.beta
    velocity0 = railgun.shell.velocity
    drag_coef = railgun.shell.drag_coef

    disp_a = 0
    disp_b = 0
    v_div = 1

    if railgun.is_specs:
        disp_a = rnd.uniform(-railgun.disp, railgun.disp)
        disp_b = rnd.uniform(-railgun.disp, railgun.disp)
        v_div = rnd.uniform(1 - railgun.v_div, 1 + railgun.v_div)

    alpha += np.radians(disp_a)
    beta += np.radians(disp_b)
    velocity0 *= v_div

    data = _calc(alpha, beta, velocity0, drag_coef)
    data.x_shell += railgun.x_railgun
    data.y_shell += railgun.y_railgun

    return data


# CONFIG
START_TIME = 0
NSTEPS = 50000
MAX_STEP = 0.01

ODE = ode(__func3)
ODE.set_integrator(
    'dopri5',
    nsteps=NSTEPS,
    max_step=MAX_STEP
)


def _calc(alpha, beta, velocity0, drag_coef):
    """

    :param beta: y_railgun-axis angle in radians
    :param velocity0: starting speed of the Shell object
    :param drag_coef: drag coefficient, aerodynamic_coefficient / weight
    :return: ODESolution
    """
    init_conditional = [  # Initial Conditional
        0,  # x0
        velocity0 * np.cos(beta),  # Vx
        0,  # y0
        velocity0 * np.sin(beta)   # Vy
    ]

    ODE.set_initial_value(init_conditional, START_TIME)  # setup initial values
    ODE.set_f_params(drag_coef)  # passing an additional argument (drag_coef) to function f

    data = ODESolution()

    y4_old = 0
    while ODE.successful():
        data.IntegrlVars.append(list(ODE.y.copy()))
        data.TimeLine.append(ODE.t)
        y1, y2, y3, y4 = ODE.y

        if y4 * y4_old < 0:  # maximum point reached
            data.Height = y3

        if y4 < 0 and y3 <= 0.0:  # the Shell has reached the surface
            data.FlightTime = ODE.t
            data.Distance = y1
            break

        y4_old = y4
        ODE.integrate(ODE.t + MAX_STEP)  # solving ODE

    data.IntegrlVars = np.array(data.IntegrlVars)
    data.TimeLine = np.array(data.TimeLine)

    data.x_shell = data.Distance * np.cos(alpha)
    data.y_shell = data.Distance * np.sin(alpha)

    return data


def _draw_plots(railgun, target, odesol: ODESolution):
    """
        Drawing plots
    :return: None
    """
    # FIGURE 1 START
    figure1 = plt.figure("Trajectory and Speed vs time graphs")
    plot1 = plt.subplot2grid((2, 2), (0, 0), colspan=2)
    plot2 = plt.subplot2grid((2, 2), (1, 0), colspan=2)

    plot1.grid(True)
    plot1.plot(odesol.IntegrlVars[:, 0], odesol.IntegrlVars[:, 2], linewidth=3, color='orange')
    plot1.set_title('Trajectory')

    v = np.array([np.sqrt(y[1] ** 2 + y[3] ** 2) for y in odesol.IntegrlVars])
    plot2.grid(True)
    plot2.plot(odesol.TimeLine, v, linewidth=3)
    plot2.set_title('Speed versus time graph')

    plt.tight_layout()

    # FIGURE 2 START
    figure2 = plt.figure("F2")
    x_railgun = railgun.x_railgun
    y_railgun = railgun.y_railgun
    x_shell, y_shell = odesol.x_shell, odesol.y_shell

    # m, n = railgun.vec
    plt.plot(x_railgun, y_railgun, marker='*', zorder=5, markersize=10)
    plt.plot((x_railgun, x_shell), (y_railgun, y_shell), linewidth=1, color='black')
    # plt.quiver(railgun.x_railgun, railgun.y_railgun, m, n, color='b', units='xy', scale=0.01)

    x_target = target.x_target
    x_target.append(x_target[0])
    y_target = target.y_target
    y_target.append(y_target[0])

    plt.plot(x_target, y_target, linewidth=2)
    plt.plot(x_shell, y_shell, marker='o', color='r')
    plt.title('Map')

    plt.grid(True)
    plt.show()
