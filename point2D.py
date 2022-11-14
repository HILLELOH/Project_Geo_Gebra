
class Point2D:
    def __init__(self, pos_x, pos_y, id):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.id = id

    def get_x(self):
        return self.pos_x

    def get_y(self):
        return self.pos_y

    def draw_circle(self, id, pos_x, pos_y, radius, canvas):  # center coordinates, radius
        x0 = pos_x - radius
        y0 = pos_y - radius
        x1 = pos_x + radius
        y1 = pos_y + radius
        return canvas.create_oval(x0, y0, x1, y1, fill="black")

    def move_point(self, id, new_x, new_y):
        pos_x = new_x
        pos_y = new_y

