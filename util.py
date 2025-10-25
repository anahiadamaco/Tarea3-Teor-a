from ast_nodes import ASTNode

def pprint_tree(node, indent=0):
    pad = '  ' * indent
    if node.value is not None:
        print(f'{pad}{node.nodetype}: {node.value}')
    else:
        print(f'{pad}{node.nodetype}')
    for c in node.children:
        pprint_tree(c, indent+1)

def to_dot(node, filename='tree.dot'):
    lines = ['digraph AST {', 'node [shape=box];']
    counter = {'n':0}
    def node_id():
        counter['n'] += 1
        return f'n{counter["n"]}'
    def walk(n):
        nid = node_id()
        label = n.nodetype + (f'\\n{n.value}' if n.value else '')
        lines.append(f'{nid} [label="{label}"];')
        for ch in n.children:
            cid = walk(ch)
            lines.append(f'{nid} -> {cid};')
        return nid
    walk(node)
    lines.append('}')
    with open(filename,'w') as f:
        f.write('\n'.join(lines))
    return filename