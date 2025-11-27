import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multiple_children(self):
        child_node = LeafNode("div", "child")
        child_node1 = LeafNode("span", "child1")
        child_node2 = LeafNode("div", "child2")
        child_node3 = LeafNode("span", "child3")
        parent_node = ParentNode("div", [child_node, child_node1, child_node2, child_node3])
        self.assertEqual(parent_node.to_html(), "<div><div>child</div><span>child1</span><div>child2</div><span>child3</span></div>")

    def test_to_html_with_multiple_children_with_props(self):
        child_node = LeafNode("div", "child", props={"class": "greeting", "id": "intro"})
        child_node1 = LeafNode("span", "child1")
        child_node2 = LeafNode("div", "child2", props={"class": "greeting", "id": "intro"})
        child_node3 = LeafNode("span", "child3")
        parent_node = ParentNode("div", [child_node, child_node1, child_node2, child_node3])
        self.assertEqual(parent_node.to_html(), '<div><div class="greeting" id="intro">child</div><span>child1</span><div class="greeting" id="intro">child2</div><span>child3</span></div>')

    def test_to_html_with_multiple_parent_children(self):
        child_node = LeafNode("div", "child")
        child_node1 = LeafNode("div", "child1")
        child_node2 = LeafNode("div", "child2")
        child_node3 = LeafNode("div", "child3", {"href": "https://www.google.com"})
        parent_node3 = ParentNode("div", [child_node3], {"href": "https://www.google.com"})
        parent_node2 = ParentNode("div", [parent_node3])
        parent_node = ParentNode("div", [child_node, child_node1, child_node2, parent_node2])


        self.assertEqual(parent_node.to_html(), '<div><div>child</div><div>child1</div><div>child2</div><div><div href="https://www.google.com"><div href="https://www.google.com">child3</div></div></div></div>')

if __name__ == '__main__':
    unittest.main()