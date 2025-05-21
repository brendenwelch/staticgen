import re
from textnode import TextNode, BlockType, block_to_block_type, text_node_to_html_node
from htmlnode import HTMLNode


def extract_markdown_images(text):
    images = re.findall(r"!\[([^\]]*)\]\(([^\)]*)", text)
    return images


def extract_markdown_links(text):
    links = re.findall(r"\[([^\]]*)\]\(([^\)]*)", text)
    return links


def text_to_textnodes(text):
    from textnode import TextNode, TextType, split_nodes_delimiter, split_nodes_image, split_nodes_link

    after_images = split_nodes_image([TextNode(text, TextType.TEXT)])
    after_links = []
    for node in after_images:
        after_links.extend(split_nodes_link([node]))
    after_code = []
    for node in after_links:
        after_code.extend(split_nodes_delimiter([node], "`", TextType.CODE))
    after_bold = []
    for node in after_code:
        after_bold.extend(split_nodes_delimiter([node], "**", TextType.BOLD))
    after_italic = []
    for node in after_bold:
        after_italic.extend(split_nodes_delimiter([node], "_", TextType.ITALIC))
    return after_italic


def markdown_to_blocks(markdown):
    splits = []
    for split in markdown.split("\n\n"):
        split = split.strip()
        if split != "":
            splits.append(split)
    return splits


def markdown_to_html_node(markdown):
    children = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        block_node = block_to_nodes(block, block_type)
        children.append(block_node)
    return HTMLNode("div", None, children, None)


def block_to_nodes(block, block_type):
    match block_type:
        case BlockType.CODE:
            return HTMLNode("code", block[3:-3], None, None)
        case BlockType.HEADING:
            level = 6
            for char in block[1:6]:
                if char == "#":
                    level -= 1
                else:
                    break
            return HTMLNode(f"h{level}", block[8-level:], None, None)
        case BlockType.QUOTE:
            dirty = block.split()
            clean = []
            for line in dirty:
                clean.append(line[2:])
            cleaned = "\n".join(clean)
            text_nodes = text_to_textnodes(cleaned)
            children = []
            for node in text_nodes:
                children.append(text_node_to_html_node(node))
            return HTMLNode("q", None, children, None)
        case BlockType.UNORDERED_LIST:
            lines = block.split()
            children = []
            for line in lines:
                text_nodes = text_to_textnodes(line[2:])
                html_nodes = []
                for node in text_nodes:
                    html_nodes.append(text_node_to_html_node(node))
                children.append(HTMLNode("li", None, html_nodes, None))
            return HTMLNode("ul", None, children, None)
        case BlockType.ORDERED_LIST:
            lines = block.split()
            children = []
            for line in lines:
                text_nodes = text_to_textnodes(line[3:])
                html_nodes = []
                for node in text_nodes:
                    html_nodes.append(text_node_to_html_node(node))
                children.append(HTMLNode("li", None, html_nodes, None))
            return HTMLNode("ol", None, children, None)
        case _:
            text_nodes = text_to_textnodes(block)
            children = []
            for node in text_nodes:
                children.append(text_node_to_html_node(node))
            return HTMLNode("p", None, children, None)
