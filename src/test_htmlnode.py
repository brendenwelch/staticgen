import sys, unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHtmlNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://link.com", "target": "_blank"})
        self.assertEqual(
            node.props_to_html(), ' href="https://link.com" target="_blank"'
        )
        print("\n[HTMLNode] props_to_html tests: success", end="")
        sys.stdout.flush()


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html(self):
        node = LeafNode("a", "link", {"href": "https://link.com", "target": "_blank"})
        self.assertEqual(
            node.to_html(), '<a href="https://link.com" target="_blank">link</a>'
        )
        print("\n[LeafNode] to_html tests: success", end="")
        sys.stdout.flush()


class TestParentNode(unittest.TestCase):
    def test_parent_to_html(self):
        child = LeafNode("a", "link", {"href": "https://link.com", "target": "_blank"})
        node = ParentNode("p", {child})
        self.assertEqual(
            node.to_html(), '<p><a href="https://link.com" target="_blank">link</a></p>'
        )
        print("\n[ParentNode] to_html (1 child) tests: success", end="")
        sys.stdout.flush()

    def test_grandparent_to_html(self):
        grandchild = LeafNode("b", "link")
        child = ParentNode("a", {grandchild}, {"href": "https://link.com", "target": "_blank"})
        node = ParentNode("p", {child})
        self.assertEqual(
            node.to_html(), '<p><a href="https://link.com" target="_blank"><b>link</b></a></p>'
        )
        print("\n[ParentNode] to_html (1 child, 1 grandchild) tests: success", end="")
        sys.stdout.flush()


if __name__ == "__main__":
    unittest.main()
