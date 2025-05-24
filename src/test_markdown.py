import sys, unittest



class TestMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        from markdown import extract_markdown_images
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        images = extract_markdown_images(text)
        self.assertEqual(images, [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])
        print("\n[Markdown] extract_markdown_images: success", end="")
        sys.stdout.flush()

    def test_extract_markdown_links(self):
        from markdown import extract_markdown_links
        text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        links = extract_markdown_links(text)
        self.assertEqual(links, [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])
        print("\n[Markdown] extract_markdown_links: success", end="")
        sys.stdout.flush()

    def test_text_to_textnodes(self):
        from markdown import text_to_textnodes
        from textnode import TextNode, TextType
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ])
        print("\n[Markdown] text_to_textnodes: success", end="")
        sys.stdout.flush()

    def test_markdown_to_blocks(self):
        from markdown import markdown_to_blocks
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        print("\n[Markdown] markdown_to_blocks: success", end="")
        sys.stdout.flush()


    def test_paragraphs(self):
        from markdown import markdown_to_html_node
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )
        print("\n[HTML] text to html (paragraphs): success", end="")
        sys.stdout.flush()

    def test_codeblock(self):
        from markdown import markdown_to_html_node
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><code>\nThis is text that _should_ remain\nthe **same** even with inline stuff\n</code></div>",
        )
        print("\n[HTML] text to html (codeblock): success", end="")
        sys.stdout.flush()


    def test_extract_title(self):
        from markdown import extract_title

        md = "# some title"
        title = extract_title(md)
        self.assertEqual(title, "some title")
        print("\n[Markdown] extract_title: success", end="")
        sys.stdout.flush()


if __name__ == "__main__":
    unittest.main()
