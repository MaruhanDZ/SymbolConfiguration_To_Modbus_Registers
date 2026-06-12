from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTextEdit,
    QFileDialog,
    QLabel,
    QLineEdit,
)

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.xml_path = ""
        self.excel_path = ""

        self.setup_ui()


    def setup_ui(self):

        self.setWindowTitle("XML Mapping Converter")
        self.setWindowIcon(QIcon("Aplication\gui\icon.ico"))
        self.resize(1000, 700)

        main_layout = QVBoxLayout(self)

        # =====================================================
        # XML FILE
        # =====================================================

        xml_layout = QHBoxLayout()

        self.xml_line = QLineEdit()
        self.xml_line.setReadOnly(True)

        # botão de selecionar arquivo xml
        self.btn_xml = QPushButton("  Select Symbol File  ")
        self.btn_xml.setFixedWidth(150)

        xml_layout.addWidget(QLabel("XML:"))
        xml_layout.addWidget(self.xml_line)
        xml_layout.addWidget(self.btn_xml)

        main_layout.addLayout(xml_layout)

        # =====================================================
        # EXCEL FILE
        # =====================================================

        excel_layout = QHBoxLayout()

        self.excel_line = QLineEdit()
        self.excel_line.setReadOnly(True)

        # botão de destino do excel
        self.btn_excel = QPushButton(" Select Destination File ")
        self.btn_excel.setFixedWidth(150)

        excel_layout.addWidget(QLabel("Excel:"))
        excel_layout.addWidget(self.excel_line)
        excel_layout.addWidget(self.btn_excel)

        main_layout.addLayout(excel_layout)

        # =====================================================
        # ACTION BUTTONS
        # =====================================================

        button_layout = QHBoxLayout()

        self.btn_refresh = QPushButton("     Update File    ")
        self.btn_refresh.setFixedWidth(150)

        self.btn_generate = QPushButton("    Export Excel File  ")        
        self.btn_generate.setFixedWidth(150)

        button_layout.addStretch()

        button_layout.addWidget(self.btn_refresh)
        button_layout.addWidget(self.btn_generate)

        main_layout.addLayout(button_layout)

        # =====================================================
        # XML TREE VIEW
        # =====================================================

        self.tree_text = QTextEdit()
        self.tree_text.setReadOnly(True)

        main_layout.addWidget(self.tree_text)

        # =====================================================
        # SIGNALS
        # =====================================================

        self.btn_xml.clicked.connect(self.select_xml)
        self.btn_excel.clicked.connect(self.select_excel)

    # =========================================================
    # FILE DIALOGS
    # =========================================================

    def select_xml(self):

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar XML",
            "",
            "XML Files (*.xml)"
        )

        if filename:
            self.xml_path = filename
            self.xml_line.setText(filename)

    def select_excel(self):

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Definir Destino",
            "",
            "Excel Files (*.xlsx)"
        )

        if filename:
            self.excel_path = filename
            self.excel_line.setText(filename)

    # =========================================================
    # PUBLIC METHODS
    # =========================================================

    def set_tree_text(self, text: str):
        self.tree_text.setPlainText(text)

    def append_log(self, text: str):
        self.tree_text.append(text)

    
if __name__ == "__main__":

    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)

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

    window.show()

    sys.exit(app.exec())