from PyQt5 import QtWidgets
from view.translation import Ui_Dialog
from PyQt5.QtWidgets import QFileDialog
from controller.translator_controller import TranslatorController
from controller.translator_controller import LocaleInfo
import os
import warnings
from openpyxl import load_workbook

from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QFileDialog, QVBoxLayout, QApplication
from PyQt5.QtCore import QStringListModel
 
class MyDialog(QtWidgets.QDialog, QtWidgets.QListView):
 
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
 
        # 이벤트 연결
        self.ui.di_search.clicked.connect(self.open_dictionary_dialog)  # 사전 파일 선택 버튼
        self.ui.xml_search.clicked.connect(self.open_xml_dialog)  # XML 파일 선택 버튼
        self.ui.pushButton_4.clicked.connect(self.start_translation)  # 번역 시작 버튼
 
        self.xml_name = None   #dictionary 입력값
        self.dict_name = None  #xml 파일 입력 값
        self.value_root = None #value가 존재하는 디렉토리 경로 - 새 폴더들이 생성되어야 할 경로
        self.locale_list = {} #국가명 가져올 리스트

        self.listModel = QStringListModel()
        self.matchList = QStringListModel()
        self.notFoundList = QStringListModel()
        
 
    # 번역사전 엑셀 파일 입력(단일)
    def open_dictionary_dialog(self):
        warnings.filterwarnings("ignore", category=UserWarning, module='openpyxl')
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open Dictionary File', "", "Excel Files (*.xlsx)")

        if not os.path.isfile(file_path):
            print(f"Input file '{file_path}' does not exist.")
            return
        
        if file_path:
            self.dict_name = file_path
            self.ui.dictionary_line.setText(file_path)

            controller = LocaleInfo(di_path=self.dict_name, xml_path="")
            self.locale_list = controller.getLocaleList()
            print("last local check:", self.locale_list)

            self.listModel.setStringList(self.locale_list)
            self.ui.listView.setModel(self.listModel)
            
 
    # XML 파일 입력
    def open_xml_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open XML File', "", "XML Files (*.xml)")
        
        if not os.path.isfile(file_path):
            print(f"Input file '{file_path}' does not exist.")
            return
        
        if file_path:
            self.xml_name = file_path
            self.ui.xml_line.setText(file_path)
 
            path_parts = file_path.replace("\\", "/").split('/')
            res_index = path_parts.index('res')
            self.value_root = '/'.join(path_parts[:res_index + 1])
 
            print(self.xml_name)
            print(self.value_root)
 
    # translation 실행
    def start_translation(self):
        if not self.dict_name or not self.xml_name:
            print("Please select both translation and XML files.")
            return
       
        controller = TranslatorController(di_path=self.dict_name, xml_path=self.xml_name, base_dir=self.value_root)
        controller.translate()

        self.matchList.setStringList(controller.getMatched())
        self.notFoundList.setStringList(controller.getNotFound())
        self.ui.match_list.setModel(self.matchList)
        self.ui.not_found_list.setModel(self.notFoundList)

        print("Translation completed.")
 
 
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MyDialog()  
    window.show()
    sys.exit(app.exec_())