import turtle

screen = turtle.Screen()
artist = turtle.Turtle()
artist.hideturtle()
artist.penup()
artist.speed('fastest')
artist.setpos(0, -305)

turtle_list = [artist]
branch_ends = []

artist.pendown()
artist.left(90)
artist.forward(150)
end = artist.pos()
branch_ends.append((end, 200, 90))


class Branches:
    def __init__(self, ends_list, pen, color, left_angle, right_angle):
        self.right_angle = right_angle
        self.left_angle = left_angle
        self.points = ends_list
        self.point = self.points[0]
        self.size = self.point[1]
        self.start_angle = self.point[2]
        self.color = color
        self.pen = pen
        self.pen.pensize(2)
        self.pen.speed('fastest')
        self.pen.hideturtle()
        self.draw_all()

    def draw(self):
        self.pen.pencolor(self.color)
        self.pen.penup()
        self.new_line("left")
        self.new_line("right")

        branch_ends.remove(self.point)

    def new_line(self, side):
        self.pen.seth(self.start_angle)
        if side == "right":
            self.pen.right(self.right_angle)
        elif side == "left":
            self.pen.left(self.left_angle)
        self.pen.goto(self.point[0])

        self.pen.pendown()
        self.pen.forward(self.size * (2/3))
        line_end = self.pen.pos()
        heading = self.pen.heading()
        # I added 5 to the heading to make it turn just a little to the left
        branch_ends.append((line_end, self.size * (2/3), heading+15))

    def draw_all(self):
        for point in self.points:
            self.point = point
            self.size = self.point[1]
            self.start_angle = self.point[2]
            self.draw()


def branches(iterations, left_angle, right_angle):
    for num in range(iterations):
        num = turtle.Turtle()
        turtle_list.append(num)
        Branches(branch_ends[0:], num, "dark green", left_angle, right_angle)


branches(8, 15, 60)    # now able to adjust angles

screen.exitonclick()
