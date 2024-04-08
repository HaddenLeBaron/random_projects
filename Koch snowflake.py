import turtle
from random import choice

screen = turtle.Screen()
artist = turtle.Turtle()
artist.hideturtle()
artist.penup()
artist.speed('fastest')
artist.setpos(-150, -75)

turtle_list = [artist]
lines = []
for _ in range(3):
    artist.left(60)
    artist.pendown()
    start = artist.pos()
    artist.forward(300)
    end = artist.pos()
    lines.append((start, end, 300))
    artist.right(180)


class SnowFlake:
    def __init__(self, line_list, pen, color):
        self.lines = line_list
        self.line = self.lines[0]
        self.size = self.line[2]
        self.color = color
        self.pen = pen
        self.pen.speed('fastest')
        self.pen.hideturtle()
        self.draw_all()

    def draw(self):
        self.pen.pencolor(self.color)
        self.pen.penup()
        self.pen.goto(self.line[0])
        self.pen.seth(self.pen.towards(self.line[1]))
        self.pen.pendown()
        self.new_line()
        self.pen.left(60)
        self.new_line()
        self.pen.right(120)
        self.new_line()
        self.pen.left(60)
        self.new_line()
        lines.remove(self.line)

    def new_line(self):
        line_start = self.pen.pos()
        self.pen.forward(self.size / 3)
        line_end = self.pen.pos()
        lines.append((line_start, line_end, self.size / 3))

    def draw_all(self):
        for line in self.lines:
            self.line = line
            self.size = self.line[2]
            self.draw()


def get_range(iterations):
    total_num = 0
    for i in range(iterations):
        total_num += 3 ** i
    return total_num


def koch(iterations):
    for num in range(iterations):
        num = turtle.Turtle()
        turtle_list.append(num)
        SnowFlake(lines[0:], num, "red")
        old_turtle = turtle_list[0]
        old_turtle.clear()
        turtle_list.remove(old_turtle)


koch(4)


screen.exitonclick()
