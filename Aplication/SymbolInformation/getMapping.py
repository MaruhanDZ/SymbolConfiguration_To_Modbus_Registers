if __name__ == '__main__':
    from getVariableTypes import getArrayTypes, getSimpleTypes, getUDTTypes
else:
    from SymbolInformation.getVariableTypes import getArrayTypes, getSimpleTypes, getUDTTypes
import xml.etree.ElementTree as ET

# cria algumas variaveis globais que serão compartilhadas entre todas as funções
typeArrays = []
typeUDTs = []
typeSimple = []
rows = []

# Utiliza as funções para armazenas as informações referente as variaveis nas variaveis globais
def getXMLtypesInfo(root, ns):
    # define o uso de algumas variaveis globais para armazenar os tipos
    global typeArrays
    global typeSimple
    global typeUDTs
    # Obtem informações dos arrays
    typeArrays = getArrayTypes(root, ns)
    # Obtem informações dos tipos base
    typeSimple = getSimpleTypes(root, ns)
    # Obtem informações dos UDTs
    typeUDTs = getUDTTypes(root, ns)


# função recusiva de expansão do tipo de dado, usado para obter a ordem de memória de cada variavel
def expandType(name, type):
    global typeArrays
    global typeSimple
    global typeUDTs
    global rows 
    # caso encontrar um tipo simples :
    if any(item['name'] == type for item in typeSimple):
        simple = next(item for item in typeSimple if item['name'] == type)
        rows.append({
            "path" : name,
            "type" : type,
            "typeclass" : simple.get('typeclass').upper(),
            "swapsize" : simple.get('swapsize'),
            "size" : simple.get('size'),
            "byteStart" : 0,
            "register" : 0,
            "bitoffset": simple.get('bitoffset')
        })

    # caso o tipo for udt
    if any(item['name'] == type for item in typeUDTs):
        udt = next(item for item in typeUDTs if item['name'] == type)

        for element in udt['elements']:
            expandType(f"{name}.{element['iecname']}", element['type'])

    
    # caso o tipo for array
    if any(item['name'] == type for item in typeArrays):
        array = next(item for item in typeArrays if item['name'] == type)

        elementType = array['basetype']
        minRange = int(array['startindex'])
        maxRange = int(array['stopindex'])

        for i in range(minRange, maxRange + 1):
            expandType(f"{name}[{i}]", elementType)


# recebe a lista gerada pela função expandTypes e o byte de inicio
def getSequentialMemorySpacing(rows, byteToStart):
    # Percorre as linhas para calcular os endereços em byte
    for i, row in enumerate(rows):

        # verifica se é do tipo string e puxa o size para o swapsize
        if (row.get('typeclass') == 'STRING'):
            row['swapsize'] = int(row.get('size'))

        # se está no primeiro elemento
        if i == 0:
            row['byteStart'] = byteToStart
        else:
            # obtem a ultima linha do array
            lastRow = rows[i - 1]
            # verifica se a linha anterior é um bit
            if lastRow.get('typeclass') == 'BIT':
                # Se a linha atual tmb for um bit
                if row.get('typeclass') == 'BIT':
                    #  verifica se mudou o byte vendo se a sequencia de bit é menor que a anterior
                    if (int(lastRow.get('bitoffset')) >= int(row.get('bitoffset'))):
                        row['byteStart'] = int(lastRow.get('byteStart')) + 1
                    else: # se não for maior mantem o mesmo byte
                        row['byteStart'] = int(lastRow.get('byteStart'))
                # se a linha atual não é um bit
                else:
                    row['byteStart'] = int(lastRow.get('byteStart', 0)) + 1
            else: # caso a linha anterior não for um bit, calcula utilizando o swapsize
                row['byteStart'] = (lastRow.get('byteStart', 0) + int(lastRow.get('swapsize', 0)))
        # a partir do byte, retorna o registrador
        row['register'] = int(row.get('byteStart'))//2



def getMapping(application, gvl, var):
    global rows
    rows.clear() # esvazia a lista na variavel global

    # utiliza a função recursiva para retornar as variaveis e udts e arrays na lista rows
    expandType(application + '.' + gvl + '.' + var['name'], var['type'])

    # popula os endereços das variaveis
    getSequentialMemorySpacing(rows, var['byteaddress'])

    # retorna uma copia das linhas
    return rows.copy()

        

if __name__ == "__main__":
    xmlfile = "testexml.PLC_AC500_V3.Application.xml"
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    ns = "{http://www.3s-software.com/schemas/Symbolconfiguration.xsd}"
    # exemplo de variavel a ser buscada

    # var deve ser um dicionário, no formato retornado pela função que adquire essa informação do xml
    var = {'name': 'sensor', 'type': 'T_ARRAY__0__0__OF_UDT_ANALOG_INPUT', 'access': 'ReadWrite', 'directaddress': '%ML100', 'byteaddress': 800}

    # necessário chamar essa função ao menos 1 vez para armazenar as variaveis nas variaveis globais
    getXMLtypesInfo(root, ns)

    # obtem o endereçamento
    getMapping('Application', 'GVL_TESTE', var)
    

    print('\n\n')
    for row in rows:
        print(row)

