import sys, unittest
from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter, split_nodes_image, split_nodes_link


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a text node", TextType.BOLD)
        node4 = TextNode("This is a text node", TextType.LINK)
        self.assertEqual(node2, node3)
        self.assertNotEqual(node, node3)
        self.assertNotEqual(node3, node4)
        print("\n[TextNode] operator (==) overload tests: success", end="")
        sys.stdout.flush()

    def test_text_to_html(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        print("\n[TextNode] text_to_html: success", end="")

    def test_split_nodes_delimiter(self):
        nodes = split_nodes_delimiter([TextNode("'wow', this is 'pretty' cool", TextType.TEXT)], "'", TextType.ITALIC)
        self.assertEqual(nodes, [TextNode("wow", TextType.ITALIC), TextNode(", this is ", TextType.TEXT), TextNode("pretty", TextType.ITALIC), TextNode(" cool", TextType.TEXT)])
        print("\n[TextNode] split_nodes_delimiter: success", end="")

    def test_split_nodes_image(self):
        node = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", TextType.TEXT),
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        ])
        print("\n[TextNode] split_nodes_image: success", end="")
        sys.stdout.flush()

    def test_split_nodes_link(self):
        node = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [
            TextNode("This is text with a !", TextType.TEXT),
            TextNode("rick roll", TextType.LINK, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and !", TextType.TEXT),
            TextNode("obi wan", TextType.LINK, "https://i.imgur.com/fJRm4Vk.jpeg"),
        ])
        print("\n[TextNode] split_nodes_link: success", end="")
        sys.stdout.flush()

if __name__ == "__main__":
    unittest.main()
