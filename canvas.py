import uuid
import json


class Node:
    def __init__(self, node_type, id, x=0, y=0, width=0, height=0, color="", label="", file=None, text=None):
        self.node = {"type": node_type, "id": id, "x": x, "y": y, "width": width, "height": height, "color": color}
        node_items = list(self.node.items())

        if node_type == "group":
            node_items.insert(1, ("label", label))
        elif node_type == "file":
            node_items.insert(1, ("file", file))
        elif node_type == "text":
            node_items.insert(1, ("text", text))

        self.node = dict(node_items)


class Edge:
    def __init__(self, edge_type, id, fromNode, fromSide, toNode, toSide, toEnd=None, fromEnd=None, color=""):
        self.edge = {"id": id, "fromNode": fromNode, "fromSide": fromSide, "toNode": toNode, "toSide": toSide, "color": color}

        if edge_type == "undirectional":
            self.edge["toEnd"] = toEnd
        elif edge_type == "bidirectional":
            self.edge["fromEnd"] = fromEnd


class Canvas:
    def __init__(self):
        self.canvas = {"nodes": [], "edges": []}

    def _generate_id(self):
        return uuid.uuid4().hex

    def add_node(self, node_type, filename=None, text=None, x=0, y=0, width=0, height=0, color="", label=""):
        id = self._generate_id()
        node = Node(node_type, id, x, y, width, height, color, label, file=filename, text=text)
        self.canvas["nodes"].append(node.node)

    def add_edge(self, edge_type, fromNode, fromSide, toNode, toSide, toEnd=None, fromEnd=None, color=""):
        id = self._generate_id()
        edge = Edge(edge_type, id, fromNode, fromSide, toNode, toSide, toEnd, fromEnd, color)
        self.canvas["edges"].append(edge.edge)

    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.canvas, f)


