class Shell:

    def __init__(self, weight, velocity, aerodyn_coef):
        """

        :param weight: weight of Shell object, [kg]
        :param velocity: median velocity of Shell object, [m/s]
        :param aerodyn_coef: aerodynamic coefficient (search necessary
            tables and values in the Google)
        """
        self.weight = weight
        self.velocity = velocity
        self.aerodyn_coef = aerodyn_coef

        self.drag_coef = aerodyn_coef / weight
