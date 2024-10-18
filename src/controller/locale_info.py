from model.locale_viewer import LocaleViewer

class LocaleInfo:
    def __init__(self, di_path="", xml_path=""):
        print("translation path:", di_path)
        # LocaleViewer 인스턴스 초기화
        self.translator = LocaleViewer(di_path, xml_path)

    # 입력한 translation 파일의 언어 리스트 가져오기
    def getLocaleList(self):
        return self.translator.get_country_name()
