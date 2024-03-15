class Square:

    _side = None

    def __init__(self, side):
        self.side = side

    @property
    def side(self):
        return self._side

    @side.setter
    def side(self, value):
        if value >= 0:
            self._side = value
        else:
            raise ValueError("Side should be positive")

    @property
    def area(self):
        return self.side**2

s1 = Square(2)
print(s1.side, s1.area)
