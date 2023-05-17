from Fields.Field import Field


class SphericalField(Field):
    """сферическая поверхность"""
    def __init__(self):
        super().__init__()

    def field_limitation(self, x, y):
        return -1 <= x < self.row + 1 and -1 <= y < self.columns + 1

    def next_button(self, x, y):

        if 0 <= x < self.row:
            x_ = x
        elif x == -1:
            x_ = self.row - 1
        else:
            x_ = 0

        if 0 <= y < self.columns:
            y_ = y
        elif y == -1:
            y_ = self.columns - 1
        else:
            y_ = 0

        return self.buttons[x_][y_]
