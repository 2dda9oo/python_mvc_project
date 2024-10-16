import pandas as pd
import xml.etree.ElementTree as ET



#딕셔너리 파일 로드
def load_dictionary(di_path):

    df = pd.read_excel(di_path, usecols="C,G:AN")
    language_code = ["es", "ko", "de", "zh", "fr", "it", "sv", "nb", "br", "pt", "tk", "ru", "nl", "da", "fi", "id", "sl"
    , "sk", "pl", "lv", "lt", "hu", "et", "el", "cs", "iw", "ar", "hi", "th", "bg", "ro", "is", "hr", "ja"]

    df.columns = ['content'] + language_code

    #비어있는 딕셔너리
    translation_dict = {}

    #content를 키로 language_code를 값으로 가진 딕셔너리 생성
    for _, row in df.iterrows():
        content = row['content']
        translation = row[1:].to_dict()
        translation_dict[content] = translation
        
    return translation_dict
    
#string.xml 로드
def load_xml(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    name_list = [elem.get('name') for elem in root.findall('string')]

    return name_list
