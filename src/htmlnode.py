class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is not None:
            out = ""
            for prop in self.props:
                out += f' {prop}="{self.props[prop]}"'
            return out
        else:
            return ""


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("[LeafNode] .to_html() no value")
        elif self.tag is None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("[ParentNode] .to_html() no tag")
        elif self.children is None:
            raise ValueError("[ParentNode] .to_html() no children")
        else:
            children_out = ""
            if self.children is not None:
                for child in self.children:
                    children_out += child.to_html()
            return f"<{self.tag}{self.props_to_html()}>{children_out}</{self.tag}>"
