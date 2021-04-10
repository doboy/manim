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

class Mhiddennode(VMobject):
  def __init__(self, label, radius, color, **kwargs):
    VMobject.__init__(self)
    if type(label) in (int, str):
      self.label = Text("?")
      self.hidden = Text(str(label))
    else:
      self.label = Text("?")
      self.hidden = label

    if label.text == "A":
      self.label = self.hidden

    self.circle = Circle(radius=radius, color=color, **kwargs)
    self.other_circle = Circle(radius=radius).set_fill(BLACK, opacity=1)
    self.label.move_to(self.circle.get_center())
    self.add(self.other_circle, self.label, self.circle)
    self.radius = radius

  def set_circle_color(self, color):
    self.circle.set_color(color)
    return self
