class Target:

    def __init__(self, *coordinates):
        """

        :param coordinates: set N-tuples -
            coordinates of the vertices of the target polygon
        """
        self.coordinates = coordinates  # [(x1, y1), ... , (xn, yn)]
        self.x_target = [x for x, y in self.coordinates]
        self.y_target = [y for x, y in self.coordinates]

    def is_target_hit(self, coordinates):
        """
        Original code:
            https://ru.wikibooks.org/wiki/Реализации_алгоритмов/Задача_о_принадлежности_точки_многоугольнику

        :param coordinates: set tuple (x_shell, y_shell) - impact point coordinates
        :return: bool
        """
        x_shell = coordinates[0]
        y_shell = coordinates[1]

        npol = len(self.x_target)
        is_hit = False

        i = 0
        j = npol - 1

        while i < npol:
            if (
                (((self.y_target[i] <= y_shell) and (y_shell < self.y_target[j]))
                or ((self.y_target[j] <= y_shell) and (y_shell < self.y_target[i])))
                and (((self.y_target[j] - self.y_target[i]) != 0)
                and (x_shell > ((self.x_target[j] - self.x_target[i]) * (y_shell - self.y_target[i])
                / (self.y_target[j] - self.y_target[i]) + self.x_target[i])))
            ):
                is_hit = not is_hit

            j = i
            i += 1

        return is_hit
