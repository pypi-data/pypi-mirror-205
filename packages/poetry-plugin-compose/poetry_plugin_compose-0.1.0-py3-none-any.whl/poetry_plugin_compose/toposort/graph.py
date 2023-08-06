from collections import defaultdict
from typing import Callable, List, Dict, TypeVar


T = TypeVar("T")


class Node:
    def __init__(self, data: T):
        self.data = data

    def __str__(self):
        return f"Node({str(self.data)})"

    def __repr__(self):
        return str(self)


class Edge:
    def __init__(self, from_node: Node, to_node: Node):
        self.from_node = from_node
        self.to_node = to_node


class CircularGraphException(Exception):
    def __init__(self, cycles):
        msg = "Cycles detected in graph: " + ",".join([str(cycle) for cycle in cycles])
        super(CircularGraphException, self).__init__(msg)
        self.cycles = cycles


class Graph:
    def __init__(self, key_extractor: Callable[[T], str]):
        self.nodes: Dict[str, Node] = {}
        self.edges_from: Dict[str, List[Edge]] = defaultdict(list)
        self.edges_to: Dict[str, List[Edge]] = defaultdict(list)
        self.key_extractor = key_extractor

    def add_node(self, data: T):
        self.nodes[self.key_extractor(data)] = Node(data)

    def add_nodes(self, datas: List[T]):
        for data in datas:
            self.add_node(data)

    def has_node(self, data: T):
        for node in self.nodes:
            if self.key_extractor(node) == data:
                return True
        return False

    def add_edge(self, from_data: T, to_data: T):
        edge = Edge(
            self.nodes[self.key_extractor(from_data)],
            self.nodes[self.key_extractor(to_data)],
        )
        self.edges_from[self.key_extractor(from_data)].append(edge)
        self.edges_to[self.key_extractor(to_data)].append(edge)

    def nodes_depending_on(self, data: T):
        return [edge.from_node for edge in self.edges_to[self.key_extractor(data)]]

    def node_dependencies(self, data: T):
        return [edge.to_node for edge in self.edges_from[self.key_extractor(data)]]

    def leafs(self):
        result = []
        for node in self.nodes.values():
            if not self.edges_from[self.key_extractor(node.data)]:
                result.append(node)
        return result

    def roots(self):
        result = []
        for node in self.nodes.values():
            if not self.edges_to[self.key_extractor(node.data)]:
                result.append(node)
        return result

    def detect_cycles(self):
        stack = [([], node) for node in self.nodes.values()]
        cycles = []
        while stack:
            path, node = stack.pop()
            if node in path:
                cycles.append(path)
                continue
            for dependencies in self.node_dependencies(node.data):
                stack.append(([*path, node], dependencies))
        return cycles

    def toposort(self):
        cycles = self.detect_cycles()
        if cycles:
            raise CircularGraphException(cycles)
        in_degrees = {}
        no_incoming_edge = []
        for node_data in self.nodes.keys():
            in_degrees[node_data] = len(self.node_dependencies(node_data))
            if in_degrees[node_data] == 0:
                no_incoming_edge.append(node_data)
        order = []
        while no_incoming_edge:
            node_data = no_incoming_edge.pop()
            order.append(node_data)
            for depending_on in self.nodes_depending_on(node_data):
                in_degrees[depending_on.data] -= 1
                if in_degrees[depending_on.data] == 0:
                    no_incoming_edge.append(depending_on.data)
                    in_degrees.pop(depending_on.data)
        return order
