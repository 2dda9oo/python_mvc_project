from PyQt5 import QtWidgets
from model.table_model import TableModel
from model.button_delegate import ButtonDelegate
from view.translation import Ui_Dialog

from controller.translator_controller import TranslatorController
from controller.translator_controller import LocaleInfo
import os
import warnings
from PyQt5.QtWidgets import QFileDialog, QFileDialog
from PyQt5.QtCore import QStringListModel

 
class MyDialog(QtWidgets.QDialog, QtWidgets.QListView):
 
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
 
        # 클릭 이벤트 연결
        self.ui.di_search.clicked.connect(self.open_dictionary_dialog)  # 사전 파일 선택 버튼
        self.ui.xml_search.clicked.connect(self.open_xml_dialog)  # XML 파일 선택 버튼
        self.ui.pushButton_4.clicked.connect(self.start_translation)  # translation 버튼

        #ListView set Model
        self.listModel = QStringListModel()
        self.matchList = QStringListModel()
        self.notFoundList = QStringListModel()

        #기타 전역변수들
        self.xml_name = None   #dictionary 입력값
        self.dict_name = None  #xml 파일 입력 값
        self.value_root = None #value가 존재하는 디렉토리 경로 - 새 폴더들이 생성되어야 할 경로
        self.locale_list = {} #국가명 가져올 리스트
        self.need_check_dict = {} #translator에서 전달받은, need_check_tableView에 보여줄 text목록
        self.controller = None    
        self.defaultMatchedList = [] #matched_word_listView에 보여줄 목록
        self.defaultNotFoundList = []#not_found_listView에 보여줄 목록
        self.can_translate = None #translation 버튼 작동 여부
        

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

            self.can_translate=True

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

            self.can_translate=True
 
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
        
        if not self.can_translate:
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
        self.ui.tableView_3.clicked.connect(self.handle_table_click) # Translate 버튼 클릭 이벤트
        self.can_translate = False   


    def update_table_view(self):
        data_to_display = self.get_data_from_need_check_dict()
        self.model = TableModel(data_to_display)
        self.ui.tableView_3.setModel(self.model)


        self.ui.tableView_3.setColumnWidth(0,129)  # text 열 너비
        self.ui.tableView_3.setColumnWidth(1, 130)  # english_text 열 너비
        self.ui.tableView_3.setColumnWidth(2, 60)   # convert 열 너비
        self.ui.tableView_3.verticalHeader().setVisible(False) #행 안보이게 설정
    
        # 버튼 델리게이트 설정
        button_delegate = ButtonDelegate(self.ui.tableView_3, controller=self.controller)
        self.ui.tableView_3.setItemDelegateForColumn(2, button_delegate)


    #need_check_tableView - translate 버튼 동작 구현
    def handle_table_click(self, index):
        if index.column() == 2:
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

        
        self.listModel.setStringList([])
        self.matchList.setStringList([])
        self.notFoundList.setStringList([])
        self.need_check_model = TableModel([])
        self.ui.listView.setModel(self.listModel)
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