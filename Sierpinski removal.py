import turtle
from random import choice

screen = turtle.Screen()
artist = turtle.Turtle()
artist.hideturtle()
artist.penup()
artist.speed('fastest')
artist.setpos(-150, -75)


start_points = []


class Triangle:
    def __init__(self, start_pos, size, color):
        self.size = size
        self.num_vertices = 3
        self.start_pos = start_pos
        self.color = color

    def draw(self, direction="right"):
        midpoints = []
        artist.goto(self.start_pos)
        artist.pencolor(self.color)
        artist.fillcolor(self.color)
        artist.pendown()
        artist.begin_fill()
        if direction == "backwards":
            artist.seth(-180)
        elif direction == "up":
            artist.seth(120)
        else:
            artist.seth(0)
        for _ in range(self.num_vertices):
            artist.forward(self.size/2)
            midpoints.append(artist.pos())
            artist.forward(self.size/2)
            if direction == "left" or direction == "backwards":
                artist.left(360 / self.num_vertices)
            else:
                artist.right(360 / self.num_vertices)
        midpoints = self.fix_list(direction, midpoints)
        midpoints.append(self.size/2)
        start_points.append(midpoints)

        artist.end_fill()
        artist.penup()

    @staticmethod
    def fix_list(direction, list_to_fix):
        if direction == "up":
            fixed_list = [list_to_fix[1], list_to_fix[2], list_to_fix[0]]
            return fixed_list
        elif direction == "backwards":
            fixed_list = [list_to_fix[0], list_to_fix[2], list_to_fix[1]]
            return fixed_list
        else:
            return list_to_fix


first_triangle = Triangle((-150, -75), 300, "black")
first_triangle.draw(direction="left")

second_triangle = Triangle(start_points[0][2], 150, "white")
second_triangle.draw()
start_points.remove(start_points[0])
color_list = ["yellow", "gold", "orange", "red", "maroon", "violet", "magenta", "purple", "navy", "blue", "skyblue",
              "cyan", "turquoise", "lightgreen", "green", "darkgreen", "chocolate", "brown", "gray"]
# color_list = ["white"]


def get_range(iterations):
    total_num = 0
    for i in range(iterations):
        total_num += 3 ** i
    return total_num


def serpinski(iterations):
    for i in range(get_range(iterations)):
        triangle1 = Triangle(start_points[0][0], start_points[0][3], choice(color_list))
        triangle1.draw(direction="up")
        triangle2 = Triangle(start_points[0][1], start_points[0][3], choice(color_list))
        triangle2.draw()
        triangle3 = Triangle(start_points[0][2], start_points[0][3], choice(color_list))
        triangle3.draw(direction="backwards")

        start_points.remove(start_points[0])


serpinski(4)
screen.exitonclick()
