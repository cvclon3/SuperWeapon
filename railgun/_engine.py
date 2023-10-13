import numpy as np
import numpy.random as rnd
import matplotlib.pyplot as plt
from scipy.integrate import ode


# CONST
G = 9.81


def __func(t, y, k: float):
    """
    The function of the right-hand sides of the ODE system
    (has an additional argument k)

    :param t: scipy.integrate.ode default argument, define as time, [s]
    :param y: integration variable
    :param k: drag coefficient, aerodynamic_coefficient / weight
    :return: [float, float, float, float]
    """
    global G
    y1, y2, y3, y4 = y

    return [
        y2,                 # y1' = y2
        -k * y2**3,         # y2' = -k * y2**3
        y4,                 # y3' = y4
        -k * y4**3 - G      # y4' = -k * y4**3 - g
    ]


# GlOBAL VARS
TimeLine = []
IntegrlVars = []
FlightTime, Distance, Height = 0, 0, 0
y4_old = 0


# CONFIG
MAX_TIME = 600
START_TIME = 0
NSTEPS = 50000
MAX_STEP = 0.01


def __checker(t, y):
    """
    Step handler for scipy.integrate.ode
    Using in scipy.integrate.ode.set_solout()

    :param t: scipy.integrate.ode default argument, define as time, [s]
    :param y: integration variable
    :return: int
    """
    global FlightTime, Distance, Height, y4_old
    TimeLine.append(t)
    IntegrlVars.append(list(y.copy()))
    y1, y2, y3, y4 = y

    if y4*y4_old < 0:   # maximum point reached
        Height = y3

    if y4 < 0 and y3 <= 0.0:   # the Shell has reached the surface
        FlightTime = t
        Distance = y1
        return -1

    y4_old = y4


ODE = ode(__func)
ODE.set_integrator(
    'dopri5',
    nsteps=NSTEPS,
    max_step=MAX_STEP
)
ODE.set_solout(__checker)


def __calc_shot(beta, velocity0, drag_coef) -> [np.array, np.array]:
    """

    :param beta: y_railgun-axis angle in radians
    :param velocity0: starting speed of the Shell object
    :param drag_coef: drag coefficient, aerodynamic_coefficient / weight
    :return: [np.array, np.array, float, float, float]
    """
    init_conditional = [  # Initial Conditional
        0,  # x0
        velocity0 * np.cos(beta),  # Vx
        0,  # y0
        velocity0 * np.sin(beta)   # Vy
    ]

    ODE.set_initial_value(init_conditional, START_TIME)  # setup initial values
    ODE.set_f_params(drag_coef)  # passing an additional argument (drag_coef) to function f
    ODE.integrate(MAX_TIME)  # solving ODE

    integrlVars = np.array(IntegrlVars)
    timeLine = np.array(TimeLine)
    distance = Distance
    flightTime = FlightTime
    height = Height

    return integrlVars, timeLine, distance, flightTime, height


def __draw_plots(integrlVars, timeLine, railgun, target, shell_coords):
    # FIGURE 1 START
    figure1 = plt.figure("Trajectory and Speed vs time graphs")
    plot1 = plt.subplot2grid((2, 2), (0, 0), colspan=2)
    plot2 = plt.subplot2grid((2, 2), (1, 0), colspan=2)

    plot1.grid(True)
    plot1.plot(integrlVars[:, 0], integrlVars[:, 2], linewidth=3, color='orange')
    plot1.set_title('Trajectory')

    v = np.array([np.sqrt(y[1]**2 + y[3]**2) for y in integrlVars])
    plot2.grid(True)
    plot2.plot(timeLine, v, linewidth=3)
    plot2.set_title('Speed versus time graph')

    plt.tight_layout()

    # FIGURE 2 START
    figure2 = plt.figure("F2")
    x_railgun = railgun.x_railgun
    y_railgun = railgun.y_railgun
    x_shell, y_shell = shell_coords

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


def shoot(railgun, target):
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

    integrlVars, timeLine, distance, flightTime, height = __calc_shot(beta, velocity0, drag_coef)
    x_shell = distance * np.cos(alpha) + railgun.x_railgun
    y_shell = distance * np.sin(alpha) + railgun.y_railgun

    is_hit = target.is_target_hit((x_shell, y_shell))
    is_hit_mess = 'Target is hit' if is_hit else 'Target is not hit'

    __draw_plots(integrlVars, timeLine, railgun, target, (x_shell, y_shell))

    print(
        f'SHOOT RESULT:\n'
        f'Flight time = {flightTime}\n'
        f'distance = {distance}\n'
        f'Max height = {height}\n'
        f'\n'
        f'{is_hit_mess}\n'
    )
