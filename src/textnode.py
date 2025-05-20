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
            raise ValueError


#TODO: check for matching delimiter
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if len(old_nodes) == 0:
        return []

    new_nodes = []
    for node in old_nodes:
        if delimiter not in node:
            new_nodes.append(TextNode(node, TextType.TEXT))
            continue

        if delimiter == node[0]:
            node_type = text_type
        else:
            node_type = TextType.TEXT

        splits = node.split(delimiter)
        for split in splits:
            new_nodes.append(TextNode(split, node_type))
            if node_type == text_type:
                node_type = TextType.TEXT
            else:
                node_type = text_type

    return new_nodes

