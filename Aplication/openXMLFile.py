# nome do arquivo XML a ser lido
import xml.etree.ElementTree as ET

# retorna a arvore XML a partir do arquivo
def get_xml_tree(xmlfile):
    # cria a arvore XML a partir do arquivo
    tree = ET.parse(xmlfile)
    return tree

# retorna a raiz da arvore XML
def get_xml_root(tree):
    # retorna a raiz da arvore XML
    return tree.getroot()


# teste do arquivo
if __name__ == "__main__":
    xmlfile = "testexml.PLC_AC500_V3.Application.xml"
    tree = get_xml_tree(xmlfile)
    root = get_xml_root(tree)
    # Imprime a arvore
    print('Arvore:',tree)
    # imprime a raiz 
    print('Tag:', root.tag, 'atributos:', root.attrib)
