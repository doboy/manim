from collections import defaultdict, deque
from manim import *

SQUARE_SIDE_LENGTH=1

class Mdeque(VMobject):
  def __init__(self, size, direction=RIGHT):
    VMobject.__init__(self)

    self.m_elements = deque()
    self.m_squares = []

    for i in range(size):
      if not self.m_squares:
        self.m_squares.append(Square(side_length=SQUARE_SIDE_LENGTH))
      else:
        self.m_squares.append(
          Square(side_length=SQUARE_SIDE_LENGTH).next_to(self.m_squares[-1], direction=direction, buff=0)
        )

    self.add(*self.m_squares)

  def append(self, m_element, create=False):
    if type(m_element) in (str, int):
      m_element = Text(str(m_element))
    self.m_elements.append(m_element)
    index = self.m_elements.index(m_element)
    animations = None
    if create:
      m_element.move_to(self.m_squares[index])
      animations = [Create(m_element)]
    else:
      m_element.generate_target()
      m_element.target.move_to(self.m_squares[index])
      animations = [MoveToTarget(m_element)]
    return [animations]

  def appendleft(self, m_element, create=False):
    if type(m_element) in (str, int):
      m_element = Text(str(m_element))
    self.m_elements.appendleft(m_element)
    index = self.m_elements.index(m_element)
    animations = []
    if create:
      m_element.move_to(self.m_squares[index])
      animations.append(Create(m_element))
    else:
      m_element.generate_target()
      m_element.target.move_to(self.m_squares[index])
      animations.append(MoveToTarget(m_element))

    for idx, _m_element in enumerate(self.m_elements):
      if idx == 0:
        continue
      _m_element.generate_target()
      _m_element.target.move_to(self.m_squares[idx])
      animations.append(MoveToTarget(_m_element))
    return [animations]

  def clear(self):
    animations = []
    for m_element in self.m_elements:
      animations.append(FadeOut(m_element))
    self.m_elements = []
    return [animations]

  def pop(self):
    m_element = self.m_elements.pop()
    return [
      [FadeOut(m_element)],
      m_element,
    ]

  def popleft(self, animate_fadeout=True):
    m_element = self.m_elements[0]
    self.m_elements.remove(m_element)
    animations = []
    if animate_fadeout:
      animations.append(FadeOut(m_element))
    for idx, _m_element in enumerate(self.m_elements):
      _m_element.generate_target()
      _m_element.target.move_to(self.m_squares[idx])
      animations.append(MoveToTarget(_m_element))

    return [
      animations,
      m_element,
    ]

  def __len__(self):
    return len(self.m_elements)

class Example(Scene):
  def construct(self):
    mqueue = Mdeque(5)
    self.play(Create(mqueue))
    self.play(*mqueue.append(1, create=True)[0])
    self.play(*mqueue.append(2, create=True)[0])
    text_3 = Text("3").move_to(LEFT)
    self.play(Create(text_3))
    self.play(*mqueue.append(text_3)[0])
    self.play(*mqueue.popleft()[0])
    self.play(*mqueue.pop()[0])
    self.play(*mqueue.appendleft(4, create=True)[0])
