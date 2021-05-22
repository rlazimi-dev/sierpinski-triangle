import turtle
import math
import time

canvas = turtle.Turtle()

screen_width = canvas.screen.window_width()
screen_height = canvas.screen.window_height()
canvas.screen.setworldcoordinates(0, 0, screen_width, screen_height)

"""
TODO:
- define the functions needed to make the recursive implementation possible
- triangles are equilateral - 60deg turns
- define the function
"""

class Rect:
  def __init__(self,top: int, right: int, bottom: int, left: int):
    if top < bottom:
      raise Exception('top < bottom')
    elif right < left:
      raise Exception('right < left')

    self.top = top
    self.right = right
    self.bottom = bottom
    self.left = left


def draw_rect(canvas, r):
  canvas.penup()
  canvas.goto(r.left, r.top)
  canvas.pendown()
  canvas.goto(r.right, r.top)
  canvas.goto(r.right, r.bottom)
  canvas.goto(r.left, r.bottom)
  canvas.goto(r.left, r.top)


def inscribe_triangle(canvas, r):

    height = r.top - r.bottom
    leg = (r.right - r.left) / 2

    canvas.penup()
    #go to bottom left of triangle (avoids calculating top angle twice)
    canvas.goto(
      r.left,
      r.bottom
    )
    #set the angle to reach the bottom right of the rect
    hypothenuse = math.sqrt(math.pow(height,2) + math.pow(leg,2))

    #go to top:
    #c*sin(theta) = y value of a diagonal
    #h*sin(theta) = height
    #theta = asin(height/h)
    theta = math.asin(height/hypothenuse) * (180/math.pi)
    canvas.left(theta)
    canvas.pendown()
    canvas.forward(hypothenuse)

    #go to bottom right (recall the triangle will be isoceles):
    top_angle = 180 - theta * 2
    canvas.right(theta)
    canvas.right(90 - top_angle / 2)
    canvas.forward(hypothenuse)

    #go to bottom left
    canvas.right(180 - theta)
    canvas.forward(r.right - r.left)



time.sleep(2)
