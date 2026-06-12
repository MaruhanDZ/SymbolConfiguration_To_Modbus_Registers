import xml.etree.ElementTree as ET
# verificar se o módulo está sendo importado ou executado diretamente para evitar importações circulares
if __name__ != "__main__":
    from .convertByteAddress import getByteAddress
else:
    from convertByteAddress import getByteAddress

# Retorna um dicionário com o nó Application 
def get_application(root):
    # Procura o nó NodeList e depois o nó Application dentro do NodeList.
    node_list = next(
        (elem for elem in root.iter() if elem.tag.endswith("NodeList")),
        None
    )
    # Se o nó NodeList não for encontrado, retorna None.
    if node_list is None:
        return None
    # Procura o nó Application dentro do NodeList e retorna ele. Se não for encontrado, retorna None.
    return next(
        (child for child in node_list if child.tag.endswith("Node")),
        None
    ).attrib

# Retorna um dicionário com as GVLs e suas variáveis.
def get_gvls(root):
    result = {}
    # Procura o nó NodeList e depois o nó Application dentro do NodeList.
    node_list = next(
        (elem for elem in root.iter() if elem.tag.endswith("NodeList")),
        None
    )
    # Se o nó NodeList não for encontrado, retorna um dicionário vazio.
    if node_list is None:
        return result

    # Application
    application = next(
        (child for child in node_list if child.tag.endswith("Node")),
        None
    )
    # Se o nó Application não for encontrado, retorna um dicionário vazio.
    if application is None:
        return result

        # Percorre as GVLs dentro do nó Application e adiciona elas ao dicionário de resultado, onde a chave é o nome da GVL e o valor é uma lista de dicionários com os atributos das variáveis da GVL.
    for gvl in application:
        gvl_name = gvl.attrib.get("name")

        result[gvl_name] = []

        for var in gvl:
            atributos = var.attrib.copy()

            atributos["byteaddress"] = getByteAddress(atributos.get('directaddress', '%MW0'))  # valor inicial

            result[gvl_name].append(atributos)

    return result


if __name__ == "__main__":
    xmlfile = "testexml.PLC_AC500_V3.Application.xml"
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    ns = "{http://www.3s-software.com/schemas/Symbolconfiguration.xsd}"

    # Obtém o nó Application do XML.
    application = get_application(root)
    print("Nome da Aplicação:\n", application)

    # Obtém as GVLs e suas variáveis do XML.
    gvls = get_gvls(root)
    # Imprime as GVLs e suas variáveis.
    for gvl, vars in gvls.items():
        print(f"\n{gvl}")

        for var in vars:
            print(f"  {var}")

    print("\nExemplo de acesso ao nome de uma GVL:")
    exGVL = list(gvls.items())[1][0] # converte o objeto dict_items para uma lista e acessa o nome da GVL no index 1
    print(exGVL) 

    # Exemplo de acesso as variáveis de uma gvl qual a variavel é acessada na gvl é definido pelo index 0 e o atributo é definido pela chave 'name'
    exVar = gvls[exGVL][0]['name'] # acessa a primeira variável da GVL e o nome dela
    print('\nExemplo de Acesso ao Nome de uma Variavel:\n', exVar)

    # Exemplo de como criar a estrutura até a variavel
    exPath = application['name'] + '.' + exGVL + '.' + exVar # concatena o nome da aplicação, o nome da GVL e o nome da variável para criar o caminho completo da variável
    print('\nExemplo de Acesso ao Caminho Completo da Variável:\n', exPath)
