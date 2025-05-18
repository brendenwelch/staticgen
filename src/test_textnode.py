import sys
import unittest
from textnode import TextNode, TextType


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


if __name__ == "__main__":
    unittest.main()
