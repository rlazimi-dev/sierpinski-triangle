import turtle
import math
import time
import argparse

parser = argparse.ArgumentParser(description='Draw a Sierpinski Triangle')
parser.add_argument('--depth', dest='depth', type=int, help='the amount of times to recurse')
parser.add_argument('--no-squares', dest='squares', action='store_false', help='do not draw the rectangles that represent the recursion subproblems')
parser.add_argument('--triangles', dest='triangles', action='store_true', help='draw the parent triangle before recursing')
parser.set_defaults(
  depth=6,
  squares=True,
  triangles=False
)

args = parser.parse_args()
depth = args.depth
draw_subproblems = args.squares
draw_parent_triangle = args.triangles


canvas = turtle.Turtle()

screen_width = canvas.screen.window_width()
screen_height = canvas.screen.window_height()
canvas.screen.setworldcoordinates(0, 0, screen_width, screen_height)


class Rect:
  def __init__(self, top, right, bottom, left):
    if top < bottom:
      raise Exception('top < bottom')
    elif right < left:
      raise Exception('right < left')

    self.top = top
    self.right = right
    self.bottom = bottom
    self.left = left

  def height(self):
    return self.top - self.bottom

  def width(self):
    return self.right - self.left


def draw_rect(canvas, r):
  canvas.penup()
  canvas.goto(r.left, r.top)
  canvas.pendown()
  canvas.goto(r.right, r.top)
  canvas.goto(r.right, r.bottom)
  canvas.goto(r.left, r.bottom)
  canvas.goto(r.left, r.top)


def inscribe_triangle(canvas, r):

    height = r.height()
    leg = r.width() / 2

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

    #reset direction
    canvas.right(180)


#when calling on rect, partition the rect into three subrects and assume that serp on those rects is displayed
#what's left is to return
'''
breaking up r into 3 Rects:
.__________.
|   |   |  |
|___|___|__|
|     |    |
|_____|____|
'''

def serp(canvas, r, depth=5, draw_subproblems=False, draw_bounds=False):

  if draw_bounds:
    inscribe_triangle(canvas, r)

  if depth == 0:
    inscribe_triangle(canvas,r)
  else:
    rt = Rect(
      r.top,
      r.right - r.width() / 4,
      r.top - r.height() / 2,
      r.left + r.width() / 4
    )

    rl = Rect(
      r.top - r.height() / 2,
      r.right - r.width() / 2,
      r.bottom,
      r.left
    )

    rr = Rect(
      r.top - r.height() / 2,
      r.right,
      r.bottom,
      r.left + r.width() / 2
    )

    if draw_subproblems:
      draw_rect(canvas, rt)
      draw_rect(canvas, rl)
      draw_rect(canvas, rr)

    serp(canvas, rt, depth-1, draw_subproblems, draw_bounds)
    serp(canvas, rl, depth-1, draw_subproblems, draw_bounds)
    serp(canvas, rr, depth-1, draw_subproblems, draw_bounds)


problem = Rect(
  screen_height * 0.9,
  screen_width * 0.9,
  screen_height * 0.1,
  screen_width * 0.1
)
if draw_subproblems:
  draw_rect(canvas, problem)

serp(
  canvas,
  problem,
  depth,
  draw_subproblems,
  draw_parent_triangle
)

time.sleep(10)
