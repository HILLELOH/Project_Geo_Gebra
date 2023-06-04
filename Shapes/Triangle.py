from Shapes.shapes import Shape

class Triangle(Shape):
    def __init__(self, p1, p2, p3, label):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.label = label
        self.hidden = False

    def get_p1(self):
        return self.p1

    def get_p2(self):
        return self.p2

    def get_p3(self):
        return self.p3

    def set_p1(self, p1):
        self.p1 = p1

    def set_p2(self, p2):
        self.p2 = p2

    def set_p3(self, p3):
        self.p3 = p3

    def is_hidden(self):
        return self.hidden

    def set_hidden(self, bool):
        self.hidden = bool

    def get_label(self):
        return self.label

    def __str__(self):
        return f"({self.p1.__repr__()} , {self.p2.__repr__()} , {self.p3.__repr__()})"

    def __repr__(self):
        return f"({self.p1.__repr__()} , {self.p2.__repr__()} , {self.p3.__repr__()})"


