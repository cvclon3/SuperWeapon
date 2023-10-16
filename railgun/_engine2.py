"""
e2 engine

Second version of engine for calculating math model of
flight object in the field of gravity and air resistance.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import ode


def __func2(t: float, y: list, k: float) -> list:
    """
        The function of the right-hand sides of the ODE system with the condition
    that the resistance force of a moving projectile is proportional to the square
    of its velocity with a coefficient k.
    (has an additional argument k)

    :param t: scipy.integrate.ode default argument, define as time, [s].
    :param y: integration variable.
    :param k: drag coefficient, aerodynamic_coefficient / weight.
    :return: list, that contains the values of the right-part of the system of ODE.
    """
    G = 9.81
    y1, y2, y3, y4 = y

    return [
        y2,                                         # y1' = y2
        -k * y2 * np.sqrt(y2 ** 2 + y4 ** 2),       # y2' = -k * y2 * sqrt(y2**2 + y4**2)
        y4,                                         # y3' = y4
        -k * y4 * np.sqrt(y2 ** 2 + y4 ** 2) - G    # y4' = -k * y2 * sqrt(y2**2 + y4**2) - G
    ]


def __func3(t: float, y: list, k: float) -> list:
    """
        The function of the right-hand sides of the ODE system with the condition
    that the resistance force of a moving projectile is proportional to the cube
    of its velocity with a coefficient k.
    (has an additional argument k)

    :param t: scipy.integrate.ode default argument, define as time, [s].
    :param y: integration variable.
    :param k: drag coefficient, aerodynamic_coefficient / weight.
    :return: list, that contains the values of the right-part of the system of ODE.
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
        Transport class.
        Contains necessary value for further operation after solving the system of ODE.
    """
    IntegrlVars = []    # Contains the solution of the system of ODE
    TimeLine = []       # Contains time intervals for each of the solutions of the system of ODE
    FlightTime = 0      # Shell flight time
    Distance = 0        # The distance covered by the Shell
    Height = 0          # Maximum Shell altitude

    x_shell = 0         # x coordinate of the Shell impact point
    y_shell = 0         # y coordinate of the Shell impact point


NSTEPS = 50000

ODE = ode(__func3)
ODE.set_integrator('dopri5', nsteps=NSTEPS)


def _calc(alpha: float,
          beta: float,
          velocity0: float,
          drag_coef: float,
          start_time: float = 0,
          step: float = 0.01
          ) -> ODESolution:
    """
        Calculate shoot.
    :param beta: y_railgun-axis angle in radians.
    :param velocity0: starting speed of the Shell object.
    :param drag_coef: drag coefficient, aerodynamic_coefficient / weight.
    :param start_time: initial time value.
    :param step: integration step.
    :return: ODESolution.
    """
    init_conditional = [  # Initial Conditional
        0,  # x0
        velocity0 * np.cos(beta),  # Vx
        0,  # y0
        velocity0 * np.sin(beta)   # Vy
    ]

    ODE.set_initial_value(init_conditional, start_time)  # Setup initial values
    ODE.set_f_params(drag_coef)  # Passing an additional argument (drag_coef) to function f

    data = ODESolution()

    y4_old = 0
    while ODE.successful():
        data.IntegrlVars.append(list(ODE.y.copy()))
        data.TimeLine.append(ODE.t)
        y1, y2, y3, y4 = ODE.y

        if y4 * y4_old < 0:  # Maximum point reached
            data.Height = y3

        if y4 < 0 and y3 <= 0.0:  # The Shell has reached the surface
            data.FlightTime = ODE.t
            data.Distance = y1
            break

        y4_old = y4
        ODE.integrate(ODE.t + step)  # Integrate next step

    data.IntegrlVars = np.array(data.IntegrlVars)
    data.TimeLine = np.array(data.TimeLine)

    data.x_shell = data.Distance * np.cos(alpha)    # Calculate the x coordinate of the Shell impact point
    data.y_shell = data.Distance * np.sin(alpha)    # Calculate the y coordinate of the Shell impact point

    return data


def _draw_plots(railgun_coords: tuple, target_coords: tuple, odesol: ODESolution) -> None:
    """
        Drawing plots:
    1) Trajectory and Speed vs time graphs;
    2) Illustration.
    :param railgun_coords: Get Railgun object coordinates.
    :param target_coords: Get coordinates of the nodes of the Target object.
    :param odesol: Get an ODESolution object with necessary data.
    :return: None.
    """
    ### First plot ###
    figure1 = plt.figure("Trajectory and Speed vs time graphs")
    plot1 = plt.subplot2grid((2, 2), (0, 0), colspan=2)  # Initialize first plot
    plot2 = plt.subplot2grid((2, 2), (1, 0), colspan=2)  # Initialize second plot

    plot1.grid(True)
    # Draw the trajectory of the Shell
    plot1.plot(odesol.IntegrlVars[:, 0], odesol.IntegrlVars[:, 2], linewidth=3, color='orange')
    plot1.set_title('Trajectory')

    v = np.array([np.sqrt(y[1] ** 2 + y[3] ** 2) for y in odesol.IntegrlVars])
    plot2.grid(True)
    # Draw speed vs time plot
    plot2.plot(odesol.TimeLine, v, linewidth=3, color='tab:blue')
    plot2.set_title('Speed versus time graph')

    plt.tight_layout()

    ### Second plot ###
    figure2 = plt.figure("Illustration")
    x_railgun, y_railgun = railgun_coords
    x_shell, y_shell = odesol.x_shell, odesol.y_shell

    # Draw the position of the Railgun
    plt.plot(x_railgun, y_railgun, marker='*', zorder=5, markersize=10, color='blue')
    # Draw the trajectory of the Shell
    plt.plot((x_railgun, x_shell), (y_railgun, y_shell), linewidth=1, color='black')

    x_target, y_target = target_coords
    x_target.append(x_target[0])
    y_target.append(y_target[0])

    # Draw the Target
    plt.plot(x_target, y_target, linewidth=2, color='orange')
    # Draw the Shell impact point
    plt.plot(x_shell, y_shell, marker='o', zorder=5, markersize=10, color='red')
    plt.title('Illustration')

    plt.grid(True)
    # Show plots
    plt.show()
