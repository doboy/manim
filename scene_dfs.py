from collections import defaultdict, deque

from mdeque import Mdeque
from manim import *
import networkx as nx

TEXT_SCALE = .3
SQUARE_SIDE_LENGTH = 1
DISCOVERED_COLOR = PURPLE

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
      ("C", "D"),
    ]

    max_queue_size, discovered_length = self.dfs("A", edges, animate=False)
    self.visited_mdeque = Mdeque(discovered_length).to_edge(DL)
    self.current_node_mdeque = Mdeque(1).to_edge(DR)
    self.queue_mdeque = Mdeque(max_queue_size, direction=UP).next_to(self.current_node_mdeque, direction=UP)
    self.play(
      Create(self.visited_mdeque),
      Create(self.queue_mdeque),
      Create(self.current_node_mdeque),
    )

    labels = {}
    for vertex in vertices:
      labels[vertex] = Text(vertex).set_color(WHITE).scale_in_place(.3)

    self.graph = Graph(
      vertices,
      edges,
      layout="circular",
      vertex_config={"fill_opacity": 0, "color": WHITE, "stroke_width": 5, "radius": .4},
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
      m_start_node = self.graph.vertices[start_node].copy()
      self.play(
        *self.queue_mdeque.append(m_start_node)[0],
      )

    max_queue_size = 0
    while len(queue) > 0:
      current = queue.popleft()
      if animate:
        if len(self.current_node_mdeque):
          _, m_element = self.current_node_mdeque.pop()
          visit_animations = self.visited_mdeque.append(m_element)[0]
          self.play(
            *visit_animations,
          )

        shift_animations, m_current = self.queue_mdeque.popleft(animate_fadeout=False)
        move_animations = self.current_node_mdeque.append(m_current)[0]
        self.play(
          *move_animations,
          *shift_animations
        )


      for neighbor in graph[current]:
        if neighbor not in discovered:
          discovered.add(neighbor)
          queue.append(neighbor)
          if animate:
            self.play(
              ApplyMethod(self.graph.vertices[neighbor].set_color, DISCOVERED_COLOR),
            )
            m_neighbor = self.graph.vertices[neighbor].copy()
            self.play(
              *self.queue_mdeque.append(m_neighbor)[0],
            )
          max_queue_size = max(max_queue_size, len(queue))

    return max_queue_size, len(discovered)
