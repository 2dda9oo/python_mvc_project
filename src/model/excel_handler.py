import pandas as pd
import xml.etree.ElementTree as ET

language_code = ["es", "ko", "de", "zh", "fr", "it", "sv", "nb", "br", "pt", "tk", "ru", "nl", "da", "fi", "id", "sl"
    , "sk", "pl", "lv", "lt", "hu", "et", "el", "cs", "iw", "ar", "hi", "th", "bg", "ro", "is", "hr", "ja"]


class InputTranslatrionFile:

    def __init__(self, di_path="", xml_path=""):
        self.di_path = di_path
        self.xml_path = xml_path
        
        #translator 파일의 dictionay 생성
        self.df = pd.read_excel(self.di_path, sheet_name = 'F_text translation', usecols="C,G:AN")
        self.df.columns = ['content'] + language_code

        #국가 코드 리스트
        self.countryList = pd.read_excel(self.di_path, sheet_name='F_text translation', usecols='G:AN').columns.tolist()
        #print("Locale List:", self.countryList)



    #딕셔너리 반환
    def load_dictionary(self):

        #비어있는 딕셔너리
        translation_dict = {}

        #content를 키로 language_code를 값으로 가진 딕셔너리 생성
        for _, row in self.df.iterrows():
            content = row['content']
            translation = row[1:].to_dict()
            translation_dict[content] = translation

        # 첫 번째 키와 값 출력
        first_key = next(iter(translation_dict))  # 첫 번째 키를 가져옴
        print("First key:", first_key)
        print("First value:", translation_dict[first_key])
        
        return translation_dict
    
    #국가 리스트 반환
    def load_country(self):
        locale_list = self.countryList
        return locale_list
    

    #string.xml 로드
    def load_xml(xml_path):
        tree = ET.parse(xml_path)
        root = tree.getroot()

        name_list = [elem.get('name') for elem in root.findall('string')]

        return name_list
