import os
from model.translator import Translator
from model.locale_viewer import LocaleViewer
from controller.locale_info import LocaleInfo


class TranslatorController:

    def __init__(self, di_path="dictionary.xlsx", xml_path="strings.xml", base_dir="output"):
        # model-Translator 인스턴스 초기화
        self.translator = Translator(di_path, xml_path, base_dir)
        self.xml_path = xml_path


    #번역 실행
    def translate(self):
        # 입력 파일 경로가 존재하는지 확인
        if not os.path.isfile(self.xml_path):
            print(f"Input file '{self.xml_path}' does not exist.")
            return
        #model 계층에서 번역 작업 시작
        self.translator.translate_xml()
        print("All Translation completed.")


    #확인 필요한 string들의 dictionary 반환
    def return_need_check_dict(self):
        return self.translator.need_check_dict
    
    
    #번역 파일과 매칭된 string들의 List 반환
    def getMatched(self):
        return self.translator.getMatchedList()
    

    #번역 파일과 매칭되지 않은 String들의 List 반환
    def getNotFound(self):
        return self.translator.getNotFoundList()
    
    
    #확인 필요한 string 번역 여부 결정 버튼
    def handle_btn_translate(self, index):
        self.translator.need_check_translate_btn(index)


    #번역 파일과 매칭되지 않은 String들 txt 파일로 저장
    def saveNotFoundList(self, list):
        self.translator.save_txt_file(list)


    #string.xml의 name 획득
    def getTranslatedN(self):
        return self.translator.getTranslatedName()
    
    
    #string.xml의 text content 획득
    def getTranslatedT(self):
        return self.translator.getTranslatedText()
