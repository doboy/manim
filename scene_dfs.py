# docker run --rm -it --user="$(id -u):$(id -g)" -v "$(pwd)":/manim manimcommunity/manim manim --config_file manim.cfg scene_dfs.py -q k -r 3200,1800
# [CLI]
# frame_width=12
# frame_height=38

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
GRAPH_BORDER = 5

class BFS(Scene):
  def construct(self):
    vertices = ["A", "B", "C", "D", "E", "F", "G", "J", "K"]
    edges = [
      ("A", "B"),
      ("A", "G"),
      ("B", "G"),
      ("B", "C"),
      ("C", "E"),
      ("G", "E"),
      ("G", "J"),
      ("J", "D"),
      ("J", "F"),
      ("D", "F"),
      ("D", "K"),
      ("K", "F"),
      ("J", "E"),
      ("K", "E"),
    ]

    title_text = Text("Breath First Search").shift(UP * (GRAPH_BORDER + 1)).scale_in_place(1.5)
    self.play(Write(title_text))

    max_queue_size, discovered_length = self.bfs("A", edges, animate=False)
    if max_queue_size != 4:
      raise Exception("Try again")
    self.visited_mdeque = Mdeque(discovered_length).to_edge(LEFT).shift(DOWN * GRAPH_BORDER)
    self.current_placeholder = Mval().to_edge(RIGHT).shift(DOWN * GRAPH_BORDER)
    self.queue_mdeque = Mdeque(discovered_length - 1, direction=UP).next_to(self.current_placeholder, direction=UP)
    self.play(
      Create(self.visited_mdeque),
      Create(self.queue_mdeque),
      Create(self.current_placeholder),
    )

    visited_order_text = Text("Visited Order").next_to(self.visited_mdeque, direction=DOWN).scale_in_place(.5)
    queue_text = Text("Queue").next_to(self.queue_mdeque, direction=UP).scale_in_place(.5)
    current_node_text = Text("Current").next_to(self.current_placeholder, direction=DOWN).scale_in_place(.5)
    self.play(
      Write(visited_order_text),
      Write(queue_text),
      Write(current_node_text),
    )

    labels = {}
    for vertex in vertices:
      labels[vertex] = Text(vertex).scale_in_place(.8)

    layout = {
      "A": [0, 0, 0],
      "B": [1, 2, 0],
      "C": [0, 3, 0],
      "G": [2, 1, 0],
      "E": [2, 4, 0],
      "J": [3, 1, 0],
      "D": [3, 3, 0],
      "F": [4, 1, 0],
      "K": [4, 4, 0],
    }

    for node in layout:
      layout[node][0] *= 1.5
      layout[node][1] *= 1.5

    self.graph = Graph(
      vertices,
      edges,
      layout=layout,
      vertex_type=Mhiddennode,
      vertex_config={
        "color": UNVISITED_COLOR,
        "stroke_width": 5,
        "radius": .4
      },
      labels=labels,
    )

    self.play(Create(self.graph.move_to([0, 0, 0])))
    self.bfs("A", edges, animate=True)

  def move_dot(self, line):
    return Dot(color=RED).next_to(self.code_text.submobjects[line], direction=LEFT)

  def bfs(self, start_node, edges, animate=False):
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
    m_arrow = None
    while len(queue) > 0:
      current = queue.popleft()
      if animate:
        shift_animations, m_current = self.queue_mdeque.popleft(animate_fadeout=False)
        m_current_copy = m_current.copy().move_to(self.current_placeholder).set_circle_color(CURRENT_NODE_COLOR)

        self.play(
          ApplyMethod(self.graph.vertices[current].set_circle_color, CURRENT_NODE_COLOR),
          Transform(m_current, m_current_copy),
          *shift_animations,
          run_time=0.5
        )

        self.play(
          ApplyMethod(self.graph.vertices[current].scale_in_place, 1.25),
          run_time=0.25
        )

        self.play(
          ApplyMethod(self.graph.vertices[current].scale_in_place, 1/1.25),
          run_time=0.25
        )

      for neighbor in graph[current]:
        if neighbor not in discovered:
          discovered.add(neighbor)
          queue.append(neighbor)
          if animate:
            start = self.graph.vertices[current].get_center()
            end = self.graph.vertices[neighbor].get_center()
            direction = (end - start) / np.linalg.norm(end - start)
            m_arrow = Arrow(
              self.graph.vertices[current].get_center() + direction * .2,
              self.graph.vertices[neighbor].get_center() - direction * .2,
            ).set_color(CURRENT_NODE_COLOR)

            self.graph.vertices[neighbor].hidden.move_to(self.graph.vertices[neighbor].label)
            self.play(
              GrowArrow(m_arrow),
              Transform(self.graph.vertices[neighbor].label, self.graph.vertices[neighbor].hidden),
            )

            self.play(
              FadeOut(m_arrow),
              *self.queue_mdeque.append(
                self.graph.vertices[neighbor].copy()
              )[0],
            )
          max_queue_size = max(max_queue_size, len(queue))

      if animate:
        self.visited_mdeque.append(m_current.copy().set_circle_color(VISITED_COLOR), move=True)
        animations = [
          ApplyMethod(self.graph.vertices[current].set_circle_color, VISITED_COLOR),
          Transform(m_current, self.visited_mdeque.m_elements[-1]),
        ]
        self.play(
          *animations,
          run_time=0.5
        )


    if animate:
      self.wait(5)

    return max_queue_size, len(discovered)
