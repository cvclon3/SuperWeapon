import numpy as np
from numpy import linalg

from railgun.shell import Shell
from railgun._engine import shoot
from railgun._engine2 import _calc_setup, _draw_plots


class Railgun:
    alpha = 0
    beta = 0

    shell = None

    x_railgun, y_railgun = 0, 0
    vec = None

    def __init__(self, specs=None):
        """

        :param specs: set specs dictionary
            {
                'Dispersion': %degrees%,
                'V_Deviation': %percent/100%  # deviation from initial speed
            }
            for current Railgun object
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
    ):
        """

        :param line1: tuple (A1, B1, C1)
        :param line2: tuple (A2, B2, C2)
        :param vec: tuple (m, n)
        :return:
        """
        a = np.array([line1[:2], line2[:2]])
        b = np.array(line1[2:] + line2[2:])
        b = np.dot(-1, b)

        self.x_railgun, self.y_railgun = linalg.solve(a, b)
        self.vec = np.array(vec)

    def load(self, shell: Shell):
        """

        :param shell: load Shell object to the railgun
        :return: int
        """
        self.shell = shell

    def rotate(self, alpha: float, beta: float):
        """

        :param alpha: x_railgun-axis angle in degrees
        :param beta: y_railgun-axis angle in degrees
        :return: int
        """
        alpha = np.radians(alpha)

        rotation_mtx = np.array([
            [np.cos(alpha), -np.sin(alpha)],
            [np.sin(alpha),  np.cos(alpha)]
        ])

        m_vec, n_vec = np.dot(rotation_mtx, self.vec)

        rad = np.arctan2(n_vec, m_vec)
        if rad < 0:
            rad += 2

        self.alpha = rad
        self.beta = np.radians(beta)
        self.vec = np.array([m_vec, n_vec])

    def shoot(self, target):
        """
            e1 version
        :param target: selected Target object
        :return:
        """
        shoot(railgun=self, target=target)

    def fire(self, target):
        """
            e2 version
        :param target: selected Target object
        :return:
        """
        data = _calc_setup(self)
        is_hit = target.is_target_hit((data.x_shell, data.y_shell))
        is_hit_mess = 'Target is hit' if is_hit else 'Target is not hit'

        print(
            f'SHOOT RESULT:\n'
            f'Flight time = {data.FlightTime}\n'
            f'distance = {data.Distance}\n'
            f'Max height = {data.Height}\n'
            f'\n'
            f'{is_hit_mess}\n'
        )

        _draw_plots(railgun=self, target=target, odesol=data)
