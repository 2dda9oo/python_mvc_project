import os
from model.translator import Translator
from model.translator import LocaleViewer

class TranslatorController:
    def __init__(self, di_path="dictionary.xlsx", xml_path="strings.xml", base_dir="output"):
        # Translator 인스턴스 초기화
        self.translator = Translator(di_path, xml_path, base_dir)

    def translate(self, input_file):
        # 입력 파일 경로가 존재하는지 확인
        if not os.path.isfile(input_file):
            print(f"Input file '{input_file}' does not exist.")
            return
        
        print(f"Translating file: {input_file}")
        self.translator.translate_xml(input_file)
        print("Translation completed.")


class LocaleInfo:
    def __init__(self, di_path="", xml_path=""):
        print("translation path:", di_path)
        #LocaleViewr 인스턴스 초기화
        self.translator = LocaleViewer(di_path, xml_path)

    #입력한 translation 파일의 언어 리스트 get
    def getLocaleList(self):
        return self.translator.get_country_name()
