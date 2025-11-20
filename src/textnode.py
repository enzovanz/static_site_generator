from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "**text**"
    ITALIC = "_text_"
    CODE = "`text`"
    LINK = "[text](url)"
    IMAGE = "![text](url)"


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
        