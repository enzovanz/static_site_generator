class HTMLNode():
    def __init__(self, tag: str = None, value: str = None, children: list = None, props: dict = None):
        self.tag = tag
        self.value = value 
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:
            return ""
        return "".join(f' {k}="{self.props[k]}"' for k in self.props)
    
    def __repr__(self):
        return (
            f"Tag: {self.tag} \n"
            f"Value: {self.value} \n"
            f"Children:{self.children} \n"
            f"Props:{self.props_to_html()}"
        )
    
class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict = None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError(f"{self.__repr__()}\nHas no value")
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError(f"{self.__repr__()}\nMissing tag")
        if not self.children:
            raise ValueError(f"{self.__repr__()}\nMissing children")
        s = f"<{self.tag}{self.props_to_html()}></{self.tag}>"
        temp_s = ""
        for child in self.children:
            temp_s += child.to_html()
        return s.replace("><", f">{temp_s}<")
            


