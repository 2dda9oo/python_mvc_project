import pandas as pd
import xml.etree.ElementTree as ET

language_code = ["es", "ko", "de", "zh", "fr", "it", "sv", "nb", "br", "pt", "tk", "ru", "nl", "da", "fi", "id", "sl"
    , "sk", "pl", "lv", "lt", "hu", "et", "el", "cs", "iw", "ar", "hi", "th", "bg", "ro", "is", "hr", "ja"]

#input 경로에 따른 Excel 파일과 xml 파일 핸들링
class InputTranslatrionFile:

    def __init__(self, di_path="", xml_path=""):
        self.di_path = di_path
        self.xml_path = xml_path
        
        #translation 엑셀 파일의 dictionay 생성 
        #dictionary = {[Key : English Text], [values : spanish, korean, german, ... japan]}
        self.df = pd.read_excel(self.di_path, sheet_name = 'F_text translation', usecols="C,G:AN")
        self.df.columns = ['content'] + language_code

        #translation 엑셀 파일의 국가 리스트 생성 
        # list = [spanish, korean, german, ... japan]
        self.countryList = pd.read_excel(self.di_path, sheet_name='F_text translation', usecols='G:AN').columns.tolist()


    #content를 key로 language_code를 values으로 가진 딕셔너리 반환
    def load_dictionary(self):
        
        translation_dict = {}

        for _, row in self.df.iterrows():
            content = row['content']
            translation = row[1:].to_dict()
            translation_dict[content] = translation

        return translation_dict
    
    
    #국가 List 반환
    def load_country(self):
        return self.countryList
    

    #string.xml의 name List 반환
    def load_xml(xml_path):

        tree = ET.parse(xml_path)
        root = tree.getroot()
        name_list = [elem.get('name') for elem in root.findall('string')]

        return name_list
