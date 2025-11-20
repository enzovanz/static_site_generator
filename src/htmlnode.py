class HTMLNode():
    def __init__(self, tag: str = None, value: str = None, children: list = None, props: dict = None):
        self.tag = tag
        self.value = value 
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        prop_string = ''
        if not self.props:
            return prop_string
        for key in self.props:
            prop_string += f' {key}="{self.props[key]}"'
        return prop_string
    
    def __repr__(self):
        return f"Tag: {self.tag} \nValue: {self.value} \nChildren:{self.children} \nProps:{self.props_to_html()}"

node = HTMLNode(tag="p", value="Hello, world!", props={"class": "greeting", "id": "intro"})