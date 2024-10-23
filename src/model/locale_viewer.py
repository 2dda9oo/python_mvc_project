from .excel_handler import InputTranslatrionFile

class LocaleViewer:
    
    def __init__(self, di_path="", xml_path=""):
        self.di_path = di_path
        self.inputTranslation = InputTranslatrionFile(di_path, xml_path)

    # 언어 리스트 가져오기
    def get_country_name(self):
        return self.inputTranslation.load_country()
