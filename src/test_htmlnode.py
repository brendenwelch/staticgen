import sys
import unittest
from htmlnode import HTMLNode


class TestHtmlNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(props={"href": "https://link.com", "target": "_blank"})
        self.assertEqual(
            node.props_to_html(), ' href="https://link.com" target="_blank"'
        )
        print("[HTMLNode] props_to_html tests: success", end="")
        sys.stdout.flush()


if __name__ == "__main__":
    unittest.main()
