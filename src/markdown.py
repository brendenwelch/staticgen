import re


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
