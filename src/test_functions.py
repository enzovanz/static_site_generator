import unittest

from functions import (
        text_node_to_html_node, 
        split_nodes_delimiter, 
        extract_markdown_images, 
        extract_markdown_links, 
        split_nodes_image, 
        split_nodes_link, 
        text_to_textnodes, 
        markdown_to_blocks, 
        block_to_block_type,
        strip_markers,
        markdown_to_html_node,
    )
from textnode import TextType, BlockType, TextNode

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
        
class TestExtractMarkdownImages(unittest.TestCase):
    def test_base(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_images(text), [('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')])
    
    def test_solo(self):
        text = "![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        self.assertEqual(extract_markdown_images(text), [('rick roll', 'https://i.imgur.com/aKaOqIh.gif')])
    
    def test_two(self):
        text = "![rick roll](https://i.imgur.com/aKaOqIh.gif)!![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_images(text), [('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')])

class TestExtractMarkdownLinks(unittest.TestCase):
    def test_base(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(extract_markdown_links(text), [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])
    
    def test_solo(self):
        text = "[to boot dev](https://www.boot.dev)https://www.boot.dev"
        self.assertEqual(extract_markdown_links(text), [("to boot dev", "https://www.boot.dev")])

class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_2(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and extra text",TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and extra text", TextType.TEXT),
            ],
            new_nodes,
        )
    
    def test_split_no_image(self):
        node = TextNode("This is text with no image and extra text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("This is text with no image and extra text", TextType.TEXT)], new_nodes)

    def test_split_just_image(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")], new_nodes)
    
    def test_split_just_2_image(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png) ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"), TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")], new_nodes)

class TestSplitNodesLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_links_2(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and extra text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and extra text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_no_link(self):
        node = TextNode("This is text with no link and extra text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("This is text with no link and extra text", TextType.TEXT)], new_nodes)

    def test_split_just_link(self):
        node = TextNode("[to boot dev](https://www.boot.dev)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("to boot dev", TextType.LINK, "https://www.boot.dev")], new_nodes)
    
    def test_split_just_2_link(self):
        node = TextNode("[to boot dev](https://www.boot.dev) [to boot dev](https://www.boot.dev)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"), TextNode("to boot dev", TextType.LINK, "https://www.boot.dev")], new_nodes)


class TestTextToTextNodes(unittest.TestCase):
    def test_to_text_nodes_base(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertEqual(text_to_textnodes(text), [
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
    
    def test_to_text_nodes_links_first(self):
        text = "[link](https://boot.dev) [link](https://boot.dev) This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a"
        self.assertEqual(text_to_textnodes(text), [
                                                    TextNode("link", TextType.LINK, "https://boot.dev"),
                                                    TextNode("link", TextType.LINK, "https://boot.dev"),
                                                    TextNode(" This is ", TextType.TEXT),
                                                    TextNode("text", TextType.BOLD),
                                                    TextNode(" with an ", TextType.TEXT),
                                                    TextNode("italic", TextType.ITALIC),
                                                    TextNode(" word and a ", TextType.TEXT),
                                                    TextNode("code block", TextType.CODE),
                                                    TextNode(" and an ", TextType.TEXT),
                                                    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                                                    TextNode(" and a", TextType.TEXT),
                                                ])
        
class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
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

    def test_markdown_to_blocks_double_space(self):
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

class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        block = "# This is a heading"
        block1= "###### This is a heading"
        block2= "####### This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        self.assertEqual(block_to_block_type(block1), BlockType.HEADING)
        self.assertNotEqual(block_to_block_type(block2), BlockType.HEADING)

    def test_code(self):
        block = "```\nThis is a paragraph\nSecondLine\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote(self):
        block = ">This is a paragraph"
        block1 = "> This is a paragraph"
        block2 = "> >This is a >paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(block1), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(block2), BlockType.QUOTE)
    
    def test_ul(self):
        block = "- This is a ul\n- item\n- item"
        self.assertEqual(block_to_block_type(block), BlockType.UL)

    def test_ol(self):
        block = "1. This is a ul\n2. item\n3. item"
        block2 = "1. This is a ul\n3. item\n2. item"
        self.assertEqual(block_to_block_type(block), BlockType.OL)
        self.assertNotEqual(block_to_block_type(block2), BlockType.OL)

    def test_paragraph(self):
        block = "This is a paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

class TestStripMarkers(unittest.TestCase):
    def test_strip_quotes(self):
        block = ">FirstLine\n>SecondLine\n> ThirdLine"
        self.assertEqual(strip_markers(block, BlockType.QUOTE), "FirstLine\nSecondLine\nThirdLine")
    def test_strip_ul(self):
        block = "- FirstLine\n- SecondLine\n- ThirdLine"
        self.assertEqual(strip_markers(block, BlockType.UL), "FirstLine\nSecondLine\nThirdLine")
    def test_strip_paragraph(self):
        block = "This is **a** paragraph"
        self.assertEqual(strip_markers(block, BlockType.PARAGRAPH), "This is **a** paragraph")
    def test_strip_code(self):
        block = "```\nCode block\n```"
        self.assertEqual(strip_markers(block, BlockType.CODE), "Code block")
    def test_strip_code2(self):
        block = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        self.assertEqual(strip_markers(block, BlockType.CODE), "This is text that _should_ remain\nthe **same** even with inline stuff")
    def test_strip_ol(self):
        block = "1. FirstLine\n2. SecondLine\n3. ThirdLine"
        self.assertEqual(strip_markers(block, BlockType.OL), "FirstLine\nSecondLine\nThirdLine")
    def test_strip_heading(self):
        block = "# This is a h1"
        block4 = "#### This is a h4"
        self.assertEqual(strip_markers(block, BlockType.HEADING), "This is a h1")
        self.assertEqual(strip_markers(block4, BlockType.HEADING), "This is a h4")
    
class TestMarkdownToHTML(unittest.TestCase):
    def test_paragraphs(self):
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

    def test_codeblock(self):
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
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )

    def test_heading1(self):
        md = """# Heading 1"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>Heading 1</h1></div>")
    
    def test_heading4(self):
        md = """#### This is a crazier heading"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h4>This is a crazier heading</h4></div>")
    
    def test_heading4_break(self):
        md = """
#### This is a crazier heading
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h4>This is a crazier heading</h4></div>")
    
    def test_ul(self):
        md = """
- Item 1
- Item 2
- Item 3
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>")
    
    def test_ol(self):
        md = """
1. Item 1
2. Item 2
3. Item 3
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ol><li>Item 1</li><li>Item 2</li><li>Item 3</li></ol></div>")

    def test_blockquote(self):
        md = """
> Item 1
> Item 2
> Item 3
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><blockquote>Item 1\nItem 2\nItem 3</blockquote></div>")

    def test_all_blocks_together(self):
        md = """
# Heading 1

This is **bold** and _italic_ with `code`.

- Item 1
- Item 2

1. First
2. Second

> Quote line 1
> Quote line 2

```
Code block _raw_ and **unchanged**
second line
```

Another paragraph here.
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div>"
            "<h1>Heading 1</h1>"
            "<p>This is <b>bold</b> and <i>italic</i> with <code>code</code>.</p>"
            "<ul><li>Item 1</li><li>Item 2</li></ul>"
            "<ol><li>First</li><li>Second</li></ol>"
            "<blockquote>Quote line 1\nQuote line 2</blockquote>"
            "<pre><code>Code block _raw_ and **unchanged**\nsecond line</code></pre>"
            "<p>Another paragraph here.</p>"
            "</div>"
        )