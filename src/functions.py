from src.htmlnode import LeafNode
from src.textnode import TextType, TextNode

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(tag=None, value=text_node.text, props=None)
    if text_node.text_type == TextType.BOLD:
        return LeafNode(tag="b", value=text_node.text, props=None)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode(tag="i", value=text_node.text, props=None)
    if text_node.text_type == TextType.CODE:
        return LeafNode(tag="code", value=text_node.text, props=None)
    if text_node.text_type == TextType.LINK:
        return LeafNode(tag="a", value=text_node.text, props={"href": f"{text_node.url}"})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode(tag="img", value="", props={"src": f"{text_node.url}", "alt": f"{text_node.text}"})
    else:
        raise Exception(f"{text_node} has not a valid text type")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        if node.text.count(delimiter)%2 != 0:
            raise Exception("Invalid markdown")
        temp_list = node.text.split(delimiter)
        for i, s in enumerate(temp_list):
            if i%2 == 0 and s:
                new_node = TextNode(s, TextType.TEXT)
                new_nodes.append(new_node)
            elif s:
                new_node = TextNode(s, text_type)
                new_nodes.append(new_node)
    return new_nodes
        
