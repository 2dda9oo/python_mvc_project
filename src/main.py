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
from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5.QtWidgets import QPushButton, QStyledItemDelegate
from model.translator import Translator
from PyQt5.QtWidgets import QStyledItemDelegate, QPushButton
from PyQt5 import QtGui, QtWidgets


#needCheckTableView
class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return 3  # 체크 텍스트, 번역 텍스트, 번역 버튼

    def data(self, index, role):
        if role == Qt.DisplayRole:
            if index.column() == 0:
                return self._data[index.row()]['check_text']
            elif index.column() == 1:
                return self._data[index.row()]['check_translation_text']
            elif index.column() == 2:
                return "Translate"  # Return "Translate" for the button column
        return None

    def flags(self, index):
        if index.column() == 2:  # Translation 버튼 열
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable


class ButtonDelegate(QStyledItemDelegate):
    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self.controller = controller

    def paint(self, painter, option, index):
        super().paint(painter, option, index)

        if index.column() == 2:
            button_rect = option.rect
            button_rect.adjust(5, 5, -5, -5)  # 버튼의 크기 조정
            button_color = QtGui.QColor(200, 200, 200)  # 버튼 색상
            painter.setBrush(button_color)
            painter.drawRect(button_rect)  # 버튼 배경 그리기
            painter.setPen(Qt.black)  # 텍스트 색상
            painter.drawText(button_rect, Qt.AlignCenter, "Translate")  # 버튼 텍스트 중앙에 그리기
    
 
class MyDialog(QtWidgets.QDialog, QtWidgets.QListView):
 
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
 
        # 클릭 이벤트 연결
        self.ui.di_search.clicked.connect(self.open_dictionary_dialog)  # 사전 파일 선택 버튼
        self.ui.xml_search.clicked.connect(self.open_xml_dialog)  # XML 파일 선택 버튼
        self.ui.pushButton_4.clicked.connect(self.start_translation)  # 번역 시작 버튼

        #ListView set Model
        self.listModel = QStringListModel()
        self.matchList = QStringListModel()
        self.notFoundList = QStringListModel()

        #기타 전역변수들
        self.xml_name = None   #dictionary 입력값
        self.dict_name = None  #xml 파일 입력 값
        self.value_root = None #value가 존재하는 디렉토리 경로 - 새 폴더들이 생성되어야 할 경로
        self.locale_list = {} #국가명 가져올 리스트
        self.need_check_dict = {}
        self.controller = None    
        self.defaultMatchedList = []
        self.defaultNotFoundList = []
        


    def get_data_from_need_check_dict(self):
        return [{'check_text': v['check_text'], 'check_translation_text': v['check_translation_text']} 
                for v in self.need_check_dict.values()]

 
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

            self.controller = LocaleInfo(di_path=self.dict_name, xml_path="")
            self.locale_list = self.controller.getLocaleList()
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
       
        self.controller = TranslatorController(di_path=self.dict_name, xml_path=self.xml_name, base_dir=self.value_root)
        self.controller.translate()

        self.defaultMatchedList.extend(self.controller.getMatched())
        self.matchList.setStringList(self.defaultMatchedList)
        self.ui.match_list.setModel(self.matchList)

        self.defaultNotFoundList.extend(self.controller.getNotFound())
        self.notFoundList.setStringList(self.defaultNotFoundList)
        self.ui.not_found_list.setModel(self.notFoundList)

        print("Translation completed.")
        self.need_check_dict = self.controller.return_need_check_dict()
        self.update_table_view()  # 번역이 완료된 후 테이블 뷰 업데이트
        self.ui.pushButton_3.clicked.connect(self.save_button_click)
        self.ui.pushButton.clicked.connect(self.make_clear)
        self.ui.tableView_3.clicked.connect(self.handle_table_click) # Translation 버튼 클릭 이벤트    


    def update_table_view(self):
        data_to_display = self.get_data_from_need_check_dict()
        self.model = TableModel(data_to_display)
        self.ui.tableView_3.setModel(self.model)


        self.ui.tableView_3.setColumnWidth(0,129)  # check_text 열 너비
        self.ui.tableView_3.setColumnWidth(1, 130)  # check_translation_text 열 너비
        self.ui.tableView_3.setColumnWidth(2, 60)   # 버튼 열 너비
        self.ui.tableView_3.verticalHeader().setVisible(False) #행 안보이게 설정
    
        # 버튼 델리게이트 설정
        button_delegate = ButtonDelegate(self.ui.tableView_3, controller=self.controller)
        self.ui.tableView_3.setItemDelegateForColumn(2, button_delegate)


    #need_check_tableView - translate btn동작 구현
    def handle_table_click(self, index):
        if index.column() == 2:  # Translation 버튼이 있는 열
            row = index.row()
            self.controller.handle_btn_translate(row)
            self.some_data_change_method()

    def some_data_change_method(self):
        self.need_check_dict = self.controller.return_need_check_dict() 
        self.update_table_view()
        name = self.controller.getTranslatedN()
        text = self.controller.getTranslatedT()
        self.defaultMatchedList.append(name)
        self.matchList.setStringList(self.defaultMatchedList)
        self.defaultNotFoundList.remove(text)
        self.notFoundList.setStringList(self.defaultNotFoundList)


    def save_button_click(self):
        if self.controller.getNotFound():
            self.controller.saveNotFoundList(self.defaultNotFoundList)


    def make_clear(self):
        self.defaultMatchedList = []
        self.defaultNotFoundList = []
        self.need_check_dict = {}

        self.need_check_dict.clear()
        self.update_table_view()

        self.matchList.setStringList([])
        self.notFoundList.setStringList([])
        self.need_check_model = TableModel([])
        self.ui.match_list.setModel(self.matchList)
        self.ui.not_found_list.setModel(self.notFoundList)
        self.ui.tableView_3.setModel(self.need_check_model)
        self.xml_name = None
        self.ui.xml_line.clear()
        self.dict_name = None
        self.ui.dictionary_line.clear() 
        print("Lists have been cleared.")

    
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MyDialog()  
    window.show()
    sys.exit(app.exec_())