import xml.etree.ElementTree as ET
import re

# retorna as variaveis nativas encontradas no arquivo de symbolo
def getSimpleTypes(root, ns):
    typeSimpleElements = []
    # busca todos os elementos do tipo TypeSimple e coloca em uma lista
    for element in root.findall(".//" + ns + "TypeSimple"):
        typeSimpleElements.append(element.attrib)

    return typeSimpleElements


# retorna os arrays encontrados no arquivo de symbolo

def getArrayTypes(root, ns):
    typeArrayElements = []
    # busca todos os elementos do tipo TypeArray e coloca em uma lista
    for element in root.findall(".//" + ns + "TypeArray"):
        iecname = element.attrib.get('iecname', '')

        # coloca os limites do array em duas variaveis
        faixa = iecname.split('[')[1].split(']')[0]
        startIndex, stopIndex = faixa.split('..')

        element.attrib['startindex'] = int(startIndex)
        element.attrib['stopindex'] = int(stopIndex)

        typeArrayElements.append(element.attrib)

    return typeArrayElements


# Busca os UDTs dentro do HTML, cria um dicionário para cada UDT e 
# cria um dicionário para cada elemento dentro do udt no formato
# UDT {atributos, {subelementos{atributos}}}
def getUDTTypes(root, ns):
    udts = []

    for udt_element in root.findall(".//" + ns + "TypeUserDef"):

        udt = udt_element.attrib.copy()

        udt["elements"] = []

        for element in udt_element.findall("./" + ns + "UserDefElement"):
            udt["elements"].append(element.attrib.copy())

        udts.append(udt)

    return udts


if __name__ == "__main__":
    xmlfile = "testexml.PLC_AC500_V3.Application.xml"
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    ns = "{http://www.3s-software.com/schemas/Symbolconfiguration.xsd}"

    print("\n\n\nTipo Simples: \n")
    # Busca todos os tipos simples do arquivo e retorna uma lista de dicionários
    TypeSimplesElements = getSimpleTypes(root, ns)
    for simple in TypeSimplesElements:
        print(simple)
    
    print("\n\n\nTipo Array: \n\n\n")

    TypeArrayElements = getArrayTypes(root, ns)
    for array in TypeArrayElements:
        print(array)

    print("\n\n\nTipo UDT: \n\n\n")

    TypeUDTElements = getUDTTypes(root, ns)
    for udt in TypeUDTElements:
        print('\n\n')
        udt_no_elements = udt.copy()
        udt_no_elements.pop('elements', None)
        print(udt_no_elements, '\n')
        for var in udt['elements']:
            print(var)
    
   







