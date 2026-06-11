import openXMLFile as openXML
from SymbolInformation.getSymbolConfig import get_symbol_config_settings as SymbInfo   
from SymbolInformation.printTree import get_tree_string
from getInfo.getApplicationInfo import get_application, get_gvls



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


print('\n\n')
for gvl, vars in gvls.items():
    


    print(f"\nGVL: {gvl}")

    for var in vars:
        print(f"  Variável: {var['name']}, Endereço: {var['directaddress']}, Byte Address: {var['byteaddress']}")
