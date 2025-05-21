import re
from enum import Enum
from htmlnode import LeafNode


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"


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
            new_nodes.append(node)
        else:
            splits = node.text.split(delimiter)
            if len(splits)%2 == 0:
                raise Exception("No closing delimiter found")
            for i, split in enumerate(splits):
                if len(split) == 0:
                    continue
                out_type = TextType.TEXT if i%2 == 0 else text_type
                new_nodes.append(TextNode(split, out_type))
    return new_nodes


def split_nodes_image(old_nodes):
    from markdown import extract_markdown_images
    new_nodes = []
    if len(old_nodes) == 0:
        return new_nodes
    for node in old_nodes:
        if node.text_type != TextType.TEXT or len(node.text) == 0:
            new_nodes.append(node)
        else:
            texts = re.split(r"!\[.*?\]\(.*?\)", node.text)
            texts.append(node.text.split(")")[-1])
            images = extract_markdown_images(node.text)
            if len(images) == 0:
                new_nodes.append(node)
                continue
            for i in range(0, len(texts)):
                if len(texts[i]) != 0:
                    new_nodes.append(TextNode(texts[i], TextType.TEXT))
                if i < len(images):
                    new_nodes.append(TextNode(images[i][0], TextType.IMAGE, images[i][1]))
    return new_nodes


def split_nodes_link(old_nodes):
    from markdown import extract_markdown_links
    new_nodes = []
    if len(old_nodes) == 0:
        return new_nodes
    for node in old_nodes:
        if node.text_type != TextType.TEXT or len(node.text) == 0:
            new_nodes.append(node)
        else:
            texts = re.split(r"\[.*?\]\(.*?\)", node.text)
            links = extract_markdown_links(node.text)
            if len(links) == 0:
                new_nodes.append(node)
                continue
            for i in range(0, len(texts)):
                if len(texts[i]) != 0:
                    new_nodes.append(TextNode(texts[i], TextType.TEXT))
                if i < len(links):
                    new_nodes.append(TextNode(links[i][0], TextType.LINK, links[i][1]))
    return new_nodes


def block_to_block_type(block):
    if block.startswith("#"):
        for i in range(1, 7):
            if block[i] == " ":
                return BlockType.HEADING
            elif block[i] != "#":
                break
        return BlockType.PARAGRAPH
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    splits = block.split("\n")
    if all(map(lambda b: b.startswith(">"), splits)):
        return BlockType.QUOTE
    if all(map(lambda b: b.startswith("- "), splits)):
        return BlockType.UNORDERED_LIST
    if all(map(lambda b: b[0].isnumeric() and b[1:3] == ". ", splits)):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

