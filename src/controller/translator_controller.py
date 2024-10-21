import os
from model.translator import Translator
from model.locale_viewer import LocaleViewer
from controller.locale_info import LocaleInfo


class TranslatorController:
    def __init__(self, di_path="dictionary.xlsx", xml_path="strings.xml", base_dir="output"):
        # Translator 인스턴스 초기화
        self.translator = Translator(di_path, xml_path, base_dir)
        self.xml_path = xml_path
        print("controller init success")
        print("di_path:"+di_path+", xml_path:"+xml_path+"base_dit:"+base_dir)

    def translate(self):

        # 입력 파일 경로가 존재하는지 확인
        if not os.path.isfile(self.xml_path):
            print(f"Input file '{self.xml_path}' does not exist.")
            return
        
        print(f"xml_file: '{self.xml_path}'")
    
        #번역 시작
        need_check_dict = self.translator.translate_xml()
        print("All Translation completed.")


    def getMatched(self):
        return self.translator.getMatchedWordList()

    def getNotFound(self):
        return self.translator.getNotFoundList()

