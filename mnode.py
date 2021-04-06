from collections import defaultdict, deque
from manim import *

SQUARE_SIDE_LENGTH = 1

class Mnode(VMobject):
  def __init__(self, label, radius, color, **kwargs):
    VMobject.__init__(self)
    if type(label) in (int, str):
      self.label = Text(str(label))
    else:
      self.label = label

    self.circle = Circle(radius=radius, color=color, **kwargs)
    self.label.move_to(self.circle.get_center())
    self.add(self.label, self.circle)
    self.radius = radius

  def set_circle_color(self, color):
    self.circle.set_color(color)
    return self
