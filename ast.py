class ASTNode:
    def __init__(self, nodetype, value=None, children=None):
        self.nodetype = nodetype
        self.value = value
        self.children = children if children else []

    def add(self, node):
        self.children.append(node)

    def __repr__(self):
        return f'ASTNode({self.nodetype}, {self.value}, children={len(self.children)})'