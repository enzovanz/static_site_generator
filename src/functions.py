from src.htmlnode import LeafNode
from src.textnode import TextType, TextNode
import re

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


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        image_list = extract_markdown_images(node.text)
        original_text = node.text
        for image in image_list:
            alt_text, url = image[0], image[1]
            temp_list = original_text.split(f"![{alt_text}]({url})", 1)
            new_node = TextNode(temp_list[0], TextType.TEXT)
            new_image = TextNode(alt_text, TextType.IMAGE, url)
            if temp_list[0].strip(): # Do not append empty strings
                new_nodes.append(new_node)
            new_nodes.append(new_image)
            original_text = temp_list[1]
        if original_text:
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        link_list = extract_markdown_links(node.text)
        original_text = node.text
        for link in link_list:
            alt_text, url = link[0], link[1]
            temp_list = original_text.split(f"[{alt_text}]({url})", 1)
            new_node = TextNode(temp_list[0], TextType.TEXT)
            new_link = TextNode(alt_text, TextType.LINK, url)
            if temp_list[0].strip(): # Do not append empty strings
                new_nodes.append(new_node)
            new_nodes.append(new_link)
            original_text = temp_list[1]
        if original_text:
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def extract_markdown_images(text):
    pattern = r'!\[([^\]]+)\]\(([^)]+)\)'
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def text_to_textnodes(text):
    main_node =  TextNode(text, TextType.TEXT)
    bold_split = split_nodes_delimiter([main_node], "**", TextType.BOLD)
    italic_split = split_nodes_delimiter(bold_split, "_", TextType.ITALIC)
    code_split = split_nodes_delimiter(italic_split, "`", TextType.CODE)
    image_split = split_nodes_image(code_split)
    link_split = split_nodes_link(image_split)
    return link_split