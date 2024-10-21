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
    
        #1단계 번역 시작
        self.translator.translate_xml()
        print("Translation completed.")


        # 번역되지 않은 리스트 및 콘텐츠 리스트 가져오기
        not_found_list = self.translator.notFoundList
        content_list = self.translator.content_list
        self.start_second_stage_translation(not_found_list, content_list)

