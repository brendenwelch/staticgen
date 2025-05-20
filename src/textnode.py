from enum import Enum
from htmlnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if (
            (self.text == other.text)
            and (self.text_type == other.text_type)
            and (self.url == other.url)
        ):
            return True
        else:
            return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src":text_node.url, "alt":text_node.text})
        case _:
            raise ValueError("invalied TextType")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    if len(old_nodes) == 0:
        return new_nodes
    for node in old_nodes:
        if node.text_type != TextType.TEXT or len(node.text) == 0:
            continue
        splits = node.text.split(delimiter)
        if len(splits)%2 == 0:
            raise Exception("No closing delimiter found")
        for i, split in enumerate(splits):
            if len(split) == 0:
                continue
            out_type = TextType.TEXT if i%2 == 0 else text_type
            new_nodes.append(TextNode(split, out_type))
    return new_nodes
