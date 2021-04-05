from collections import defaultdict, deque
from manim import *

SQUARE_SIDE_LENGTH=1

class Mdeque(VMobject):
  def __init__(self, size):
    VMobject.__init__(self)

    self.elements = deque()
    self.m_elements = deque()
    self.m_squares = []

    for i in range(size):
      if not self.m_squares:
        self.m_squares.append(Square(side_length=SQUARE_SIDE_LENGTH))
      else:
        self.m_squares.append(
          Square(side_length=SQUARE_SIDE_LENGTH).next_to(self.m_squares[-1], direction=RIGHT, buff=0)
        )

    self.add(*self.m_squares)

  def append(self, element, m_element=None, create=False):
    m_element = m_element or Text(str(element))
    self.elements.append(element)
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
    return animations

  def appendleft(self, element, m_element=None, create=False):
    m_element = m_element or Text(str(element))
    self.elements.appendleft(element)
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
    return animations


  def pop(self):
    element = self.elements.pop()
    m_element = self.m_elements.pop()
    return [
      element,
      m_element,
      [FadeOut(m_element)],
    ]

  def popleft(self):
    element = self.elements[0]
    m_element = self.m_elements[0]
    self.elements.remove(element)
    self.m_elements.remove(m_element)
    animations = [FadeOut(m_element)]
    for idx, _m_element in enumerate(self.m_elements):
      _m_element.generate_target()
      _m_element.target.move_to(self.m_squares[idx])
      animations.append(MoveToTarget(_m_element))

    return [
      element,
      m_element,
      animations,
    ]

class Example(Scene):
  def construct(self):
    mqueue = Mdeque(5)
    self.play(Create(mqueue))
    self.play(*mqueue.append(1, create=True))
    self.play(*mqueue.append(2, create=True))
    text_3 = Text("3").move_to(LEFT)
    self.play(Create(text_3))
    self.play(*mqueue.append(3, text_3))
    element, m_element, animations = mqueue.popleft()
    self.play(*animations)
    element, m_element, animations = mqueue.pop()
    self.play(*animations)
    self.play(*mqueue.appendleft(1, create=True))
