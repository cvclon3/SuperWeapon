import numpy as np
import numpy.random as rnd
from numpy import linalg

from railgun.shell import Shell
from railgun._engine2 import _calc, _draw_plots, ODESolution


class Railgun:
    """Railgun main class."""
    alpha = 0
    beta = 0

    shell = None

    x_railgun, y_railgun = 0, 0
    vec = None

    def __init__(self, specs: dict = None):
        """
            Set specs for current Railgun object.
        :param specs: set specs dictionary like example:
            {
                'Dispersion': %degrees%,
                'V_Deviation': %percent/100%  # deviation from initial speed.
            }
        """
        self.is_specs = 1 if specs else 0

        if specs:
            self.disp = specs['Dispersion']
            self.v_div = specs['V_Deviation']

    def locate(
            self,
            line1: tuple[float, float, float],
            line2: tuple[float, float, float],
            vec: tuple[float, float]
            ) -> None:
        """
            Calculate the position and the direction of firing of the Railgun.
        :param line1: tuple (A1, B1, C1) - coefficient of the first line equation.
        :param line2: tuple (A2, B2, C2) - coefficient of the second line equation.
        :param vec: tuple (m, n) - direction vector.
        :return: None.
        """
        a = np.array([line1[:2], line2[:2]])
        b = np.array(line1[2:] + line2[2:])
        b = np.dot(-1, b)

        self.x_railgun, self.y_railgun = linalg.solve(a, b)
        self.vec = np.array(vec)

    def load(self, shell: Shell) -> None:
        """
            Loading the Shell object into the Railgun.
        :param shell: the Shell object, that will be fired.
        :return: None.
        """
        self.shell = shell

    def rotate(self, alpha: float, beta: float) -> None:
        """
            Turn the Railgun to the alpha angle.
        :param alpha: x_railgun-axis angle in degrees.
        :param beta: y_railgun-axis angle in degrees.
        :return: None.
        """
        alpha = np.radians(alpha)

        rotation_mtx = np.array([
            [np.cos(alpha), -np.sin(alpha)],
            [np.sin(alpha),  np.cos(alpha)]
        ])

        m_vec, n_vec = np.dot(rotation_mtx, self.vec)

        # Calculate new alpha angle
        rad = np.arctan2(n_vec, m_vec)
        self.alpha = np.degrees(rad)
        if self.alpha < 0:
            self.alpha += 360

        self.alpha = np.radians(self.alpha)
        self.beta = np.radians(beta)
        self.vec = np.array([m_vec, n_vec])

    def _calc_setup(self) -> ODESolution:
        """
            Prepare parameters for further calculating.
        :param self: Railgun object.
        :return: ODESolution.
        """
        alpha = self.alpha
        beta = self.beta
        velocity0 = self.shell.velocity
        drag_coef = self.shell.drag_coef

        disp_a = 0  # Init default Railgun dispersion for alpha angle
        disp_b = 0  # Init default Railgun dispersion for beta angle
        v_div = 1  # Init default Railgun deviation for Shell start speed

        # Check if specs for Railgun exist
        if self.is_specs:
            disp_a = rnd.uniform(-self.disp, self.disp)  # Get random value for alpha angle dispersion
            disp_b = rnd.uniform(-self.disp, self.disp)  # Get random value for alpha angle dispersion
            v_div = rnd.uniform(1 - self.v_div, 1 + self.v_div)

        alpha += np.radians(disp_a)
        beta += np.radians(disp_b)
        velocity0 *= v_div

        # Calculate the trajectory
        return _calc(alpha, beta, velocity0, drag_coef)

    def fire(self, target) -> None:
        """
            e2 version.
        :param target: selected as current target Target object.
        :return: None.
        """
        data = self._calc_setup()
        is_hit = target.is_target_hit((data.x_shell, data.y_shell))
        is_hit_mess = 'Target is hit' if is_hit else 'Target is not hit'

        print(
            f'SHOOT RESULT:\n'
            f'Flight time = {data.FlightTime}\n'
            f'Distance = {data.Distance}\n'
            f'Max height = {data.Height}\n'
            f'\n'
            f'{is_hit_mess}\n'
        )

        _draw_plots((self.x_railgun, self.y_railgun), (target.x_target, target.y_target), data)
