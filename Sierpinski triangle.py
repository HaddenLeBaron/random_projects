import turtle
from random import randint
from math import atan, pi

screen = turtle.Screen()
artist = turtle.Turtle()
artist.hideturtle()
artist.penup()
artist.speed('fast')
artist.setpos(-100, 100)


def distance(current_pos, vertex):
    x_squared = (vertex[0]-current_pos[0])**2
    y_squared = (vertex[1]-current_pos[1])**2
    dist = (x_squared + y_squared)**(1/2)
    return dist


def determine_quadrant(point):
    quadrant_determinate = 1
    if point[0] < 0:
        quadrant_determinate += 1
    if point[1] < 0:
        quadrant_determinate += 3
    if quadrant_determinate == 5:
        return 3
    else:
        return quadrant_determinate


def angle_finder(point):
    quadrant = determine_quadrant(point)
    angle_from_origin = atan(point[0]/point[1]) * (180/pi)
    if quadrant % 2 == 0:
        adjusted_angle = 180 * (quadrant / 2) + angle_from_origin
    elif quadrant == 3:
        adjusted_angle = 180 + angle_from_origin
    else:
        adjusted_angle = angle_from_origin
    return adjusted_angle


def angle_between(angle1, angle2):
    angle = abs(angle1 - angle2)
    if angle > 180:
        angle = angle - 180
    return angle


artist.pendown()
vertices = []


def fractalize(num_vertices):
    for _ in range(num_vertices):
        vertices.append(artist.pos())
        artist.forward(200)
        artist.right(360/num_vertices)

    for _ in range(2000):
        artist.penup()
        position = artist.pos()
        corner_num = randint(0, num_vertices-1)
        print(corner_num)
        corner = vertices[corner_num]
        if str(corner) == str(position):
            print('try again')
            pass
        else:
            artist.pencolor('green')
            angle_towards = artist.towards(corner)
            artist.seth(angle_towards)
            artist.forward(((num_vertices-2)/(num_vertices-1)*(distance(position, corner))))
            artist.dot()


fractalize(3)
screen.exitonclick()
