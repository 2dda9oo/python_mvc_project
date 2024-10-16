import xml.etree.ElementTree as ET
import os
import model.excel_handler as EH
from datetime import datetime 

# 파일 경로(예시) - view단에서 입력받은 값을 사용하도록 추후 옮겨야함
di_path = "dictionary.xlsx"
xml_path = "strings.xml"

excel_dictionary = EH.load_dictionary(di_path)
language_list = EH.load_xml(xml_path)
application_name = language_list[0] #name 리스트의 가장 첫번째 값은 안드로이드 앱 이름인 듯

base_dir = "string.xml 파일을 input 할 때 value 디렉토리가 존재하던 경로가 되어야 할 듯"


def translation_file(application_name):
    
    #국가코드 가져오기(35개)
    language_code = list(excel_dictionary[next(iter(excel_dictionary))].keys())

    #각 언어 코드에 해당하는 디렉토리와 xml 파일 생성
    for code in language_code:

        #번역 결과 xml 저장할 디렉토리
        direcotry_name = f"values-{code}"
        #위 디렉토리가 저장될 경로
        output_dir = os.path.join(base_dir, direcotry_name)
        #동일한 이름의 디렉토리가 없다면 생성
        os.makedirs(output_dir, exist_ok=True)


        #XML 파일 저장
        current_date = datetime.now().strftime("%Y-%m-%d")
        tree = ET.ElementTree("resources")
        output_file = os.path.join(output_dir, f"{current_date}-{application_name}.xml")
        tree.write(output_file, encoding="utf-8", xml_declaration=True)