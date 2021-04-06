# -r 1900,600

from collections import defaultdict, deque

from mdeque import Mdeque
from mval import Mval
from mnode import Mnode, Mhiddennode
import numpy as np
from manim import *
import networkx as nx
from colors import *

UNVISITED_COLOR = RED_C
VISITED_COLOR = GREEN_SCREEN
CURRENT_NODE_COLOR = YELLOW_C

class BFS(Scene):
  def construct(self):
    # vertices = ["A", "B", "C", "D", "E", "F", "G", "J", "K"]
    # edges = [
    #   ("A", "B"),
    #   ("A", "G"),
    #   ("B", "G"),
    #   ("B", "C"),
    #   ("C", "E"),
    #   ("G", "E"),
    #   ("G", "J"),
    #   ("J", "D"),
    #   ("J", "F"),
    #   ("D", "F"),
    #   ("D", "K"),
    #   ("K", "F"),
    #   ("J", "E"),
    #   ("K", "E"),
    # ]
    vertices = ["A", "B", "C", "D"]
    edges = [
      ("A", "B"),
      ("A", "C"),
      # ("C", "D"),
    ]

    max_queue_size, discovered_length = self.dfs("A", edges, animate=False)
    self.visited_mdeque = Mdeque(discovered_length).to_edge(DL)
    self.current_placeholder = Mval().to_edge(DR)
    self.queue_mdeque = Mdeque(max_queue_size, direction=UP).next_to(self.current_placeholder, direction=UP)
    self.play(
      Create(self.visited_mdeque),
      Create(self.queue_mdeque),
      Create(self.current_placeholder),
    )

    visited_order_text = Text("Visited Order").next_to(self.visited_mdeque, direction=UP).scale_in_place(.5)
    queue_text = Text("Queue").next_to(self.queue_mdeque, direction=UP).scale_in_place(.5)
    current_node_text = Text("Current Node").next_to(self.current_placeholder, direction=DOWN).scale_in_place(.5)
    self.play(
      Create(visited_order_text),
      Create(queue_text),
      Create(current_node_text),
    )

    labels = {}
    for vertex in vertices:
      labels[vertex] = Text(vertex).scale_in_place(.8)

    self.graph = Graph(
      vertices,
      edges,
      layout="circular",
      vertex_type=Mhiddennode,
      vertex_config={
        "fill_opacity": 0,
        "color": UNVISITED_COLOR,
        "stroke_width": 5,
        "radius": .4
      },
      labels=labels,
    )

    self.play(Create(self.graph))
    self.dfs("A", edges, animate=True)

  def dfs(self, start_node, edges, animate=False):
    """Returns max_queue_size, discovered_nodes"""
    graph = defaultdict(set)
    for (start, end) in edges:
      graph[start].add(end)
      graph[end].add(start)

    discovered = set([start_node])
    queue = deque([start_node])

    if animate:
      self.play(
        *self.queue_mdeque.append(self.graph.vertices[start_node].copy())[0],
      )

    max_queue_size = 0
    current = None
    m_current = None
    while len(queue) > 0:
      current = queue.popleft()
      if animate:
        shift_animations, m_current = self.queue_mdeque.popleft(animate_fadeout=False)
        m_current_copy = m_current.copy().move_to(self.current_placeholder).set_circle_color(CURRENT_NODE_COLOR)

        self.play(
          ApplyMethod(self.graph.vertices[current].set_circle_color, CURRENT_NODE_COLOR),
          Transform(m_current, m_current_copy),
          *shift_animations,
        )

      for neighbor in graph[current]:
        if neighbor not in discovered:
          discovered.add(neighbor)
          queue.append(neighbor)
          if animate:
            start = self.graph.vertices[current].get_center()
            end = self.graph.vertices[neighbor].get_center()
            direction = (end - start) / np.linalg.norm(end - start)

            arrow = Arrow(
              self.graph.vertices[current].get_center() + direction * .2,
              self.graph.vertices[neighbor].get_center() - direction * .2,
            ).set_color(CURRENT_NODE_COLOR)

            self.play(
              GrowArrow(arrow)
            )

            self.graph.vertices[neighbor].hidden.move_to(self.graph.vertices[neighbor].label)
            self.play(
              Transform(self.graph.vertices[neighbor].label, self.graph.vertices[neighbor].hidden),
              FadeOut(arrow),
            )

            self.play(
              *self.queue_mdeque.append(
                self.graph.vertices[neighbor].copy()
              )[0],
            )
          max_queue_size = max(max_queue_size, len(queue))

      if animate:
        self.visited_mdeque.append(m_current.copy().set_circle_color(VISITED_COLOR), move=True)
        self.play(
          ApplyMethod(self.graph.vertices[current].set_circle_color, VISITED_COLOR),
          Transform(m_current, self.visited_mdeque.m_elements[-1]),
        )


    if animate:
      self.wait(5)

    return max_queue_size, len(discovered)
