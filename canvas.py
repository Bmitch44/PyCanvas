import uuid
import json

class Node:
    def __init__(self, node_type, id, x=0, y=0, width=0, height=0, color="", label="", filename="", filepath="", text=""):
        self.node = {"type": node_type, "id": id, "x": x, "y": y, "width": width, "height": height, "color": color}

        if node_type == "file":
            self.node["file"] = filename

        if node_type == "text":
            self.node["text"] = text

        if node_type == "group":
            self.node["label"] = label
    
    def _get_cords(self, node_map, padding=20, position="right"):
        x_min = 0
        x_max = 0
        y_min = 0
        y_max = 0
        for node in node_map.values():
            if node.node["x"] < x_min:
                x_min = node.node["x"]
            if node.node["x"] + node.node["width"] > x_max:
                x_max = node.node["x"] + node.node["width"]
            if node.node["y"] < y_min:
                y_min = node.node["y"]
            if node.node["y"] + node.node["height"] > y_max:
                y_max = node.node["y"] + node.node["height"]

        if position == "left":
            x_min -= padding
            return x_min, y_min
        elif position == "top":
            y_min -= padding
            return x_min, y_min
        elif position == "bottom":
            y_max += padding
            return x_min, y_max
        else:
            x_max += padding
            return x_max, y_min


class GroupNode(Node):
    def __init__(self, id, node_map, children=None, color="", label=""):
        super().__init__("group", id=id, color=color, label=label)
        self.node["x"], self.node["y"], self.node["width"], self.node["height"] = self._get_cords(node_map, children)

    def _get_cords(self, node_map, children, alignment="h-line"):
        x = 0
        y = 0
        width = 0
        height = 0
        if children is None:
            print("No children")
            return x, y, width, height
        for child_id in children:
            child = node_map[child_id]
            if not child.node["id"] in node_map:
                raise ValueError("Child ID not in node map")
            if child.node["x"] < x:
                x = child.node["x"]
            if child.node["y"] < y:
                y = child.node["y"]
            if alignment == "h-line":
                width += child.node["width"]
                if child.node["height"] > height:
                    height = child.node["height"]
            elif alignment == "v-line":
                height += child.node["height"]
                if child.node["width"] > width:
                    width = child.node["width"]
        return x, y, width, height


class FileNode(Node):
    def __init__(self, id, node_map, filename, filepath, text, width, height, color):
        super().__init__("file", id, width=width, height=height, filename=filename, filepath=filepath, text=text, color=color)
        self.node["x"], self.node["y"] = self._get_cords(node_map)
        self._save_file(filepath, text)

    def _save_file(self, filepath, text):
        with open(filepath, 'w') as f:
            f.write(text)


class TextNode(Node):
    def __init__(self, id, node_map, text, width, height, color):
        super().__init__("text", id, width=width, height=height, text=text, color=color)
        self.node["x"], self.node["y"] = self._get_cords(node_map)


class Edge:
    def __init__(self, edge_type, id, fromNode, fromSide, toNode, toSide, toEnd=None, fromEnd=None, color=""):
        self.edge = {"id": id, "fromNode": fromNode, "fromSide": fromSide, "toNode": toNode, "toSide": toSide, "color": color}

        if edge_type == "undirectional":
            self.edge["toEnd"] = toEnd
        elif edge_type == "bidirectional":
            self.edge["fromEnd"] = fromEnd

class Canvas:
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.canvas = {"nodes": [], "edges": []}
        self.node_map = {}

    def _generate_id(self):
        return uuid.uuid4().hex

    def add_node(self, node_type, children=None, filename="", text="", x=0, y=0, width=100, height=100, color="", label=""):
        id = self._generate_id()
        if node_type == "file":
            node = FileNode(id=id, node_map=self.node_map, filename=filename, filepath=self.root_dir + filename, text=text, width=width, height=height, color=color)
        elif node_type == "group":
            node = GroupNode(node_map=self.node_map, children=children, id=id, color=color, label=label)
        else:
            node = TextNode(id=id, node_map=self.node_map, text=text, width=width, height=height, color=color)
        # node = Node(node_type, id, x, y, width, height, color, label, filepath=self.root_dir + filename, filename=filename, text=text)
        self.node_map[id] = node
        self.canvas["nodes"].append(node.node)
        return id

    def add_edge(self, edge_type, fromNode_id, fromSide, toNode_id, toSide, toEnd=None, fromEnd=None, color=""):
        if fromNode_id not in self.node_map or toNode_id not in self.node_map:
            raise ValueError("One or both node IDs are invalid.")
        id = self._generate_id()
        edge = Edge(edge_type, id, fromNode_id, fromSide, toNode_id, toSide, toEnd, fromEnd, color)
        self.canvas["edges"].append(edge.edge)

    def save_to_file(self, filename):
        with open(self.root_dir + filename, 'w') as f:
            json.dump(self.canvas, f)



