from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD_TEXT = "**Bold text**"
    ITALIC_TEXT = "_Italic text_"
    CODE_TEXT = "`Code text`"
    LINK = "[anchor text](url)"
    IMAGE = "![alt text](url)"


class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, TextNode):
        if self.text == TextNode.text and self.text_type == TextNode.text_type and self.url == TextNode.url:
            return True
        return False
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
        