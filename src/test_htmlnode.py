import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(tag="p", value="Hello, world!", props={"class": "greeting", "id": "intro"})
        self.assertEqual(node.props_to_html(), ' class="greeting" id="intro"')
    
    def test_print(self):
        node = HTMLNode(tag="p", value="Hello, world!", props={"class": "greeting", "id": "intro"})
        self.assertEqual(node.__repr__(), f"Tag: {node.tag} \nValue: {node.value} \nChildren:{node.children} \nProps:{node.props_to_html()}")

    def test_print2(self):
        children_node = HTMLNode(tag="a", value="Hi, world!", props={"class": "greeting", "id": "intro"})
        node = HTMLNode(tag="p", value="Hello, world!", children=[children_node], props={"class": "greeting", "id": "intro"})
        self.assertEqual(node.__repr__(), f"Tag: {node.tag} \nValue: {node.value} \nChildren:{node.children} \nProps:{node.props_to_html()}")

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_p(self):
        node = LeafNode("b", "This is a bold text")
        self.assertEqual(node.to_html(), "<b>This is a bold text</b>")
    
    def test_leaf_to_html_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

if __name__ == '__main__':
    unittest.main()