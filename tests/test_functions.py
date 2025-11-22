import unittest

from src.functions import text_node_to_html_node, split_nodes_delimiter
from src.textnode import TextType, TextNode

class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")
        self.assertEqual(html_node.to_html(), "<b>This is a bold text node</b>")

    def test_text_italic(self):
        node = TextNode("This is a italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a italic text node")
        self.assertEqual(html_node.to_html(), "<i>This is a italic text node</i>")

    def test_text_code(self):
        node = TextNode("This is a code text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code text node")
        self.assertEqual(html_node.to_html(), "<code>This is a code text node</code>")

    def test_text_link(self):
        node = TextNode("This is a link text node", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link text node")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})
        self.assertEqual(html_node.to_html(), '<a href="https://www.google.com">This is a link text node</a>')

    def test_text_image(self):
        node = TextNode("This is a image text node", TextType.IMAGE, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://www.google.com", "alt": "This is a image text node"})
        self.assertEqual(html_node.to_html(), '<img src="https://www.google.com" alt="This is a image text node"></img>')

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" word", TextType.TEXT)])

    def test_bold(self):
        node = TextNode("This is text with a **bold block** _word_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT), TextNode("bold block", TextType.BOLD), TextNode(" _word_", TextType.TEXT)])
    
    def test_exception(self):
        with self.assertRaises(Exception) as cm:
            node = TextNode("This is text with a `code block word", TextType.TEXT)
            new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(str(cm.exception), "Invalid markdown")

    def test_code_twice(self):
        node = TextNode("This is `text` with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is ", TextType.TEXT), TextNode("text", TextType.CODE), TextNode(" with a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" word", TextType.TEXT)])
    
    def test_code_twice_beggining(self):
        node = TextNode("`This is text` with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is text", TextType.CODE), TextNode(" with a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" word", TextType.TEXT)])

    def test_list_nodes(self):
        node = TextNode("`This is text` with a `code block` word", TextType.TEXT)
        node2 = TextNode("`This is text`", TextType.CODE)
        node3 = TextNode("**This is text**", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node, node2, node3], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text", TextType.CODE), 
            TextNode(" with a ", TextType.TEXT), 
            TextNode("code block", TextType.CODE), 
            TextNode(" word", TextType.TEXT), 
            TextNode("`This is text`", TextType.CODE), 
            TextNode("**This is text**", TextType.BOLD)])
        
    def test_list_nodes_multiple(self):
        node = TextNode("`This is text` with a `code block` word", TextType.TEXT)
        node2 = TextNode("`This is text` this is not bold", TextType.TEXT)
        node3 = TextNode("**This is text**", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node, node2, node3], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text", TextType.CODE), 
            TextNode(" with a ", TextType.TEXT), 
            TextNode("code block", TextType.CODE), 
            TextNode(" word", TextType.TEXT), 
            TextNode("This is text", TextType.CODE), 
            TextNode(" this is not bold", TextType.TEXT), 
            TextNode("**This is text**", TextType.BOLD)])