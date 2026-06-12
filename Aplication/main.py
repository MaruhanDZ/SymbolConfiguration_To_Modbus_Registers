import openXMLFile as openXML
from SymbolInformation.getSymbolConfig import get_symbol_config_settings as SymbInfo   
from SymbolInformation.printTree import get_tree_string
from getInfo.getApplicationInfo import get_application, get_gvls
from SymbolInformation.getMapping import getMapping, getXMLtypesInfo

from excelHandler.workbookStyle import configTab, treeTab, createHeader, appendVar, adjustWidth, convertToNumber

from excelHandler.handleWorkbook import getWorkbook



# obtem o arquivo xml
path = "testexml.PLC_AC500_V3.Application.xml"

# obtem o arquivo xml e a raiz do arquivo xml
tree = openXML.get_xml_tree(path)
root = openXML.get_xml_root(tree)

ns = "{http://www.3s-software.com/schemas/Symbolconfiguration.xsd}" # Nome da raiz do namespace

# obtem e imprime as configurações do projeto
config_settings = SymbInfo(root, ns)
print('Configurações do projeto: \n', config_settings)

tree_str = get_tree_string(root)
# imprime a arvore de variaveis do projeto
print('\nÁrvore de variáveis do projeto:\n',tree_str)

# obtem o objeto de aplicação (Application)
application = get_application(root)

# obtem os GVLs e suas variáveis, e imprime o nome do GVL, nome da variável, endereço direto e endereço em byte
gvls = get_gvls(root)

# verifica quantas gvls tem no arquivo
num_tabs = len(list(gvls))

# cria o workbook
wb = getWorkbook()

# cria a aba de informações
projectTAB = wb.active
projectTAB = configTab(projectTAB, config_settings, "PROJECT")

# cria a aba da arvore de variaveis
treeTAB = wb.create_sheet()
treeTAB = treeTab(treeTAB, tree_str, "TREE")


print('\n\n')

# obtem as informações que serão utilizadas para gerar 
getXMLtypesInfo(root, ns)

# cabiçalho das abas do excel
headers = ["path", "typeclass", "size", "byteStart", "bitoffset", "register"]


# percorre as gvls e cria uma aba para cada gvl
for gvl, vars in gvls.items():

    excelTab = wb.create_sheet(title=gvl)

    # Cabeçalho para as variaveis
    createHeader(excelTab, headers)
    
    
    # Percorre as variáveis da GVL
    for var in vars:

        mappings = getMapping(application.get('name', 'error'), gvl, var)
        appendVar(excelTab, headers, mappings)
        
    # Filtro automático
    excelTab.auto_filter.ref = excelTab.dimensions
    adjustWidth(excelTab, 200, 10)
    convertToNumber(excelTab)

wb.save("Tags_CLP.xlsx")

