class Shell:
    """Shell main class."""

    def __init__(self, weight: float, velocity: float, aerodyn_coef: float):
        """
            Setup the initial parameters of the Shell object.
        :param weight: weight of Shell object, [kg].
        :param velocity: median velocity of Shell object, [m/s].
        :param aerodyn_coef: aerodynamic coefficient (search for thenecessary tables and values on Google).
        """
        self.weight = weight
        self.velocity = velocity
        self.aerodyn_coef = aerodyn_coef

        self.drag_coef = aerodyn_coef / weight
