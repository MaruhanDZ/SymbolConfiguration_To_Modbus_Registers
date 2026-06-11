import xml.etree.ElementTree as ET

# retorna as informações de configuração de símbolos encontradas no XML no formato de dicionário
def get_symbol_config_settings(root, ns):
    symbol_config_settings = []
    for element in root.findall('.//' + ns + "SymbolConfigObject"):
        symbol_config_settings.append(element.attrib)
    return symbol_config_settings[0]

if __name__ == "__main__":
    xmlfile = "testexml.PLC_AC500_V3.Application.xml"
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    ns = "{http://www.3s-software.com/schemas/Symbolconfiguration.xsd}"
    settings = get_symbol_config_settings(root, ns)
    print(settings)

