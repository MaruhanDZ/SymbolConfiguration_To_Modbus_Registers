import xml.etree.ElementTree as ET

def get_tree_string(root):
    """
    Retorna a árvore do NodeList como uma string.
    """
    
    def build_tree(node, lines, prefix="", is_last=True):
        attrs = ", ".join(f'{k}="{v}"' for k, v in node.attrib.items())

        connector = "└── " if is_last else "├── "
        lines.append(prefix + connector + attrs)

        children = [child for child in node if child.tag.endswith("Node")]
        new_prefix = prefix + ("    " if is_last else "│   ")

        for i, child in enumerate(children):
            build_tree(
                child,
                lines,
                new_prefix,
                i == len(children) - 1
            )

    node_list = next(
        (elem for elem in root.iter() if elem.tag.endswith("NodeList")),
        None
    )

    if node_list is None:
        return ""

    lines = []

    for i, node in enumerate(node_list):
        build_tree(node, lines, "", i == len(node_list) - 1)

    return "\n".join(lines)


if __name__ == "__main__":
    xmlfile = "testexml.PLC_AC500_V3.Application.xml"

    tree = ET.parse(xmlfile)
    root = tree.getroot()

    tree_str = get_tree_string(root)

    print(tree_str)