from collections import defaultdict, deque
from manim import *

SQUARE_SIDE_LENGTH=1

class Mval(VMobject):
  def __init__(self):
    VMobject.__init__(self)
    self.m_element = None
    self.m_square = Square(side_length=SQUARE_SIDE_LENGTH)
    self.add(self.m_square)

  def set(self, m_new, create=False, animate_fadeout=True):
    m_old = self.m_element
    animations = []

    if m_old and animate_fadeout:
      animations.append(FadeOut(m_old))

    if m_new:
      if type(m_new) in (str, int):
        m_new = Text(str(m_new))

      if create:
        m_new.move_to(self.m_square)
        animations.append(Create(m_new))
      else:
        m_new.generate_target()
        m_new.target.move_to(self.m_square)
        animations.append(MoveToTarget(m_new))

    self.m_element = m_new
    return animations, m_old

class Example(Scene):
  def construct(self):
    m_val = Mval()
    self.play(Create(m_val))
    animations = m_val.set(None)[0]
    if animations: self.play(*animations)

    text = Text("B").shift(UP)
    self.play(Create(text))
    animations = m_val.set(text)[0]
    if animations: self.play(*animations)

    text = Text("C").shift(UP)
    self.play(Create(text))
    animations = m_val.set(text)[0]
    if animations: self.play(*animations)

