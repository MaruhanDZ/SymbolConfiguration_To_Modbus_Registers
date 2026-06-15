import openXMLFile as openXML
from SymbolInformation.getSymbolConfig import get_symbol_config_settings as SymbInfo   
from SymbolInformation.printTree import get_tree_string
from getInfo.getApplicationInfo import get_application, get_gvls
from SymbolInformation.getMapping import getMapping, getXMLtypesInfo
from excelHandler.workbookStyle import configTab, treeTab, createHeader, appendVar, adjustWidth, convertToNumber
from excelHandler.handleWorkbook import getWorkbook
from gui.mainWindow import MainWindow
import sys
from PySide6.QtWidgets import QApplication, QMessageBox

ns = "{http://www.3s-software.com/schemas/Symbolconfiguration.xsd}" # Nome da raiz do namespace

# função para abrir o arquivo
from PySide6.QtWidgets import QMessageBox

# função para abrir o arquivo
def getXML():
    global window
    global config_settings
    global tree_str
    global application
    global gvls
    global num_tabs
    global root
    global ns

    if window.xml_path == "":
        QMessageBox.warning(
            window,
            "No file selected",
            "Please select an XML file before continuing."
        )
        return

    try:
        # obtem o arquivo xml e a raiz do arquivo xml
        tree = openXML.get_xml_tree(window.xml_path)
        root = openXML.get_xml_root(tree)

        # obtem e imprime as configurações do projeto
        config_settings = SymbInfo(root, ns)
        print('Configurações do projeto:\n', config_settings)

        tree_str = get_tree_string(root)

        # imprime a arvore de variaveis do projeto
        print('\nÁrvore de variáveis do projeto:\n', tree_str)

        # obtem o objeto de aplicação (Application)
        application = get_application(root)

        # obtem os GVLs e suas variáveis
        gvls = get_gvls(root)

        # verifica quantas gvls tem no arquivo
        guiTreeText = (
            f'Generated Tree From File: {window.xml_path}.\n\n{tree_str}'
        )

        num_tabs = len(list(gvls))
        window.set_tree_text(guiTreeText)

        QMessageBox.information(
            window,
            "File Loaded",
            f"XML file loaded successfully!\n\n"
            f"GVLs found: {num_tabs}"
        )

    except Exception as e:
        QMessageBox.critical(
            window,
            "Error Loading XML",
            f"Unable to process the XML file.\n\n"
            f"File:\n{window.xml_path}\n\n"
            f"Error:\n{str(e)}"
        )
 

def generateExcelFile():
    global window
    global config_settings
    global tree_str
    global application
    global gvls
    global num_tabs
   
    if window.excel_path == "":
        QMessageBox.warning(
            window,
            "No File Selected",
            "Please select the destination path for the Excel file before continuing."
        )
        return
    if root is not None: # variavel que tem o caminho e nome para salvar o excel
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
        # salva o arquivo
        # salva o arquivo
        try:
            wb.save(window.excel_path)

            QMessageBox.information(
                window,
                "File Saved",
                f"The Excel file was saved successfully.\n\n"
                f"Location:\n{window.excel_path}"
            )

        except Exception as e:
            QMessageBox.critical(
                window,
                "Failed to Save File",
                f"The file could not be saved.\n\n"
                f"Details:\n{str(e)}"
            )




### ----------------------- Interface Grafica ------------------------
        
# Inicializa a engine
app = QApplication(sys.argv)
# Cria a janela
window = MainWindow()

# Texto de exemplo para teste
window.set_tree_text(
"""
Please select a SymbolConfiguration file to start!

After loading the file, you will be able to check the project variable tree as follows:

Application
 ├── GlobalVariableList_1
 │    ├── Variable_1
 │    ├── Variable_2
 │    └── Variable_3
 ├── GlobalVariableList_2
 │    ├── Struct_1 (UDT)
 │    │    ├── Member_1
 │    │    ├── Member_2
 │    │    └── Member_3
 │    ├── Variable_1
 │    └── Variable_2
 └── GlobalVariableList_N
      ├── Variable_1
      ├── Variable_2
      └── Variable_N

"""
    )

window.btn_refresh.clicked.connect(getXML) # função chamada quando clica o botão de atualizar o arquivo
window.btn_generate.clicked.connect(generateExcelFile) # função chamada quando clica no botão de gerar excel

# mostra a janela
window.show()

# caso apertar o bot
sys.exit(app.exec())
