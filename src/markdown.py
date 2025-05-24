import re
from textnode import BlockType, block_to_block_type, text_node_to_html_node
from htmlnode import HTMLNode, ParentNode, LeafNode


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
    return ParentNode("div", children)


def block_to_nodes(block, block_type):
    match block_type:
        case BlockType.CODE:
            return ParentNode("code", [LeafNode(None, block[3:-3])])
        case BlockType.HEADING:
            level = 1
            for char in block[1:6]:
                if char == "#":
                    level += 1
                else:
                    break
            return LeafNode(f"h{level}", block[level+1:])
        case BlockType.QUOTE:
            dirty = block.split("\n")
            clean = []
            for line in dirty:
                clean.append(line[2:])
            cleaned = "\n".join(clean)
            text_nodes = text_to_textnodes(cleaned)
            children = []
            for node in text_nodes:
                children.append(text_node_to_html_node(node))
            return ParentNode("blockquote", children)
        case BlockType.UNORDERED_LIST:
            lines = block.split("\n")
            children = []
            for line in lines:
                text_nodes = text_to_textnodes(line[2:])
                html_nodes = []
                for node in text_nodes:
                    html_nodes.append(text_node_to_html_node(node))
                children.append(ParentNode("li", html_nodes))
            return ParentNode("ul", children)
        case BlockType.ORDERED_LIST:
            lines = block.split("\n")
            children = []
            for line in lines:
                text_nodes = text_to_textnodes(line[3:])
                html_nodes = []
                for node in text_nodes:
                    html_nodes.append(text_node_to_html_node(node))
                children.append(ParentNode("li", html_nodes))
            return ParentNode("ol", children)
        case _:
            text_nodes = text_to_textnodes(block)
            for node in text_nodes:
                node.text = node.text.replace("\n", " ")
            children = []
            for node in text_nodes:
                children.append(text_node_to_html_node(node))
            return ParentNode("p", children)


def extract_title(markdown):
    for line in markdown.split("\n"):
        if line[:2] == "# ":
            return line[2:].strip()
    raise Exception("no title found")


