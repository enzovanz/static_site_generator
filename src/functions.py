from htmlnode import ParentNode, LeafNode
from textnode import TextType, BlockType, TextNode
import re
import os
import shutil

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

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    cleaned = [b.strip() for b in blocks if b.strip()]
    return cleaned

def block_to_block_type(block):
    if bool(re.match(r'^#{1,6}\s', block)):
        return BlockType.HEADING
    elif bool(re.match(r'^```[\s\S]*?```', block)):
        return BlockType.CODE
    elif bool(re.match(r'^>\s?', block)):
        return BlockType.QUOTE
    elif bool(re.match(r'^-\s', block)):
        return BlockType.UL
    else:
        lines = block.splitlines()
        numbers = []
        for line in lines:
            match = re.match(r'^(\d+)\.\s', line)
            if match:
                numbers.append(int(match.group(1)))

        if numbers and all(b == a + 1 for a, b in zip(numbers, numbers[1:])):
            return BlockType.OL

        return BlockType.PARAGRAPH

def strip_markers(block, block_type):
    lines = [b for b in block.split("\n") if b]
    if block_type == BlockType.QUOTE:
        lines_cleaned = [re.sub(r'^>\s?', '', line) for line in lines]
        return "\n".join(lines_cleaned)
    if block_type == BlockType.UL:
        lines_cleaned = [re.sub(r'^-\s', '', line) for line in lines]
        return "\n".join(lines_cleaned)
    if block_type == BlockType.OL:
        lines_cleaned = [re.sub(r'^(\d+)\.\s', '', line) for line in lines]
        return "\n".join(lines_cleaned)
    if block_type == BlockType.CODE:
        if len(lines) > 2:
            if lines[0] == '```':
                del lines[0]
            if lines[-1] == '```':
                del lines[-1]
        return "\n".join(lines)
    if block_type == BlockType.HEADING:
        count = 0
        while block[count] == "#":
            count += 1
        return block[count + 1:]
    if block_type == BlockType.PARAGRAPH:
        return block.replace("\n", " ")

def text_to_children(text):
    childrens = []
    text_nodes = text_to_textnodes(text)
    for text_node in text_nodes:
        childrens.append(text_node_to_html_node(text_node))
    return childrens

def text_to_list_children(text):
    childrens = []
    text_nodes = []
    for item in text.split("\n"):
        text_nodes.extend(text_to_textnodes(item))
    for text_node in text_nodes:
        children = text_node_to_html_node(text_node)
        parent = ParentNode("li", [children])
        childrens.append(parent)
    return childrens

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    all_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        block_text = strip_markers(block, block_type)
        if block_type == BlockType.PARAGRAPH:
            children = text_to_children(block_text)
            node = ParentNode("p", children)
        elif block_type == BlockType.QUOTE:
            children = text_to_children(block_text)
            node = ParentNode("blockquote", children)
        elif block_type == BlockType.CODE:
            code_text_node = TextNode(block_text, TextType.CODE)
            code_node = text_node_to_html_node(code_text_node)
            node = ParentNode("pre", [code_node])
        elif block_type == BlockType.HEADING:
            c = 0
            children = text_to_children(block_text)
            while block[c] == "#":
                c += 1
            node = ParentNode(f"h{c}", children)
        elif block_type == BlockType.UL:
            children = text_to_list_children(block_text)
            node = ParentNode(f"ul", children)
        elif block_type == BlockType.OL:
            children = text_to_list_children(block_text)
            node = ParentNode(f"ol", children)
        all_nodes.append(node)
    return ParentNode("div", all_nodes)

def copy_files(src, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.mkdir(dest)
    recursive_copy(src, dest)

def recursive_copy(src, dest):
    for item in os.listdir(src):   
        file_path_source = os.path.join(src, item)
        file_path_destination = os.path.join(dest, item)
        if os.path.isfile(file_path_source):
            shutil.copy(file_path_source, file_path_destination)
        else:
            os.mkdir(file_path_destination)
            recursive_copy(file_path_source, file_path_destination)

def extract_title(markdown):
    for line in markdown.split("\n"):
        if len(line) > 2 and line[0] == "#" and line[1] == " ":
            return line[2:]
    raise Exception("Markdown has to have a title")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r", encoding="utf-8") as md_file:
        md_content = md_file.read()

    with open(template_path, "r", encoding="utf-8") as html_file:
        html_page = html_file.read()

    html_content = markdown_to_html_node(md_content).to_html()
    title = extract_title(md_content)
    html_full_page = (
        html_page
        .replace("{{ Title }}", title)
        .replace("{{ Content }}", html_content)
    )       
    html_full_page = (
        html_full_page
        .replace('href="/', f'href="{basepath}')
        .replace('src="/', f'src="{basepath}')
    ) 
    
    folder, filename = os.path.split(dest_path)
    os.makedirs(folder, exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(html_full_page)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    dir_list = os.listdir(dir_path_content)
    for dir in dir_list:
        src = os.path.join(dir_path_content, dir)
        dest = os.path.join(dest_dir_path, dir)
        if os.path.isfile(src):
            folder, filename = os.path.split(dest)
            dest = os.path.join(folder, filename.replace(".md", ".html"))
            generate_page(src, template_path, dest, basepath)
        else:
            generate_pages_recursive(src, template_path, dest, basepath)