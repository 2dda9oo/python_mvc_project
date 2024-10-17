import xml.etree.ElementTree as ET
import os
import model.excel_handler as EH
from .excel_handler import language_code
from model.excel_handler import InputTranslatrionFile

class Translator:

    def __init__(self, di_path="dictionary.xlsx", xml_path="strings.xml", base_dir=""):
        self.di_path = di_path
        self.xml_path = xml_path
        self.base_dir = base_dir
        self.matchedWordList = [] #번역된 name List들
        self.notFoundList = [] #번역안된 name List들
        self.output_paths = {}
        self.inputTranslation = InputTranslatrionFile(di_path, xml_path)
        
    def translate_xml(self):
        output_paths = {}
        excel_dictionary = EH.load_dictionary(self.di_path)
        # 처음 5개의 키와 값 출력
        for i, (key, value) in enumerate(excel_dictionary.items()):
            if i < 5:  # 처음 5개 항목만 출력
                print(f"Key: {key}, Value: {value}")
            else:
                break

        language_code = list(excel_dictionary[next(iter(excel_dictionary))].keys())
        input_file_name = os.path.basename(self.xml_path)
        print("input_file_name: "+input_file_name)

        self.create_output_directories(language_code, input_file_name)

        content_list = list(excel_dictionary.keys())
        print("content_list: " + ", ".join(content_list[:3]))

        tree = ET.parse(self.xml_path)
        root = tree.getroot()

        print("이제 번역시작함")
        self.process_xml_strings(root, content_list, excel_dictionary)

        self.save_xml_file(language_code, root)

     #각 언어 코드에 해당하는 디렉토리와 xml 파일 생성
    def create_output_directories(self, language_code, input_file_name):
        for code in language_code:
            directory_name = f"values-{code}"
            output_dir = os.path.join(self.base_dir, directory_name)
            os.makedirs(output_dir, exist_ok=True)

            root = ET.Element("resources")
            tree = ET.ElementTree(root)
            # 언어별로 새로운 XML 파일 생성 준비
            output_path = os.path.join(output_dir, input_file_name)
            tree.write(output_path, encoding="utf-8", xml_declaration=True)

            self.output_paths[code] = output_path

    #번역
    def process_xml_strings(self, root, content_list, excel_dictionary):
        for string_element in root.findall("string"):
            name = string_element.get('name')
            text = string_element.get('text')
            #name이 존재한다면, 번역 데이터 만들기
            if name in content_list:
                translations = excel_dictionary[name]
                for code in language_code:
                    translation = translations.get(code)
                    if translation:
                        new_string = ET.Element("string", name=name)
                        new_string.text = translation

                        print("name , text: "+new_string)

                        self.save_xml_file(new_string, code)

            else:
                print(f"{name} is not found in the dictionary.")
                
                for code in language_code:
                    self.notFoundList.append(name)
                    new_string = ET.Element("string", name=name)
                    new_string.text = text

                    self.save_xml_file(new_string, code)
            

    #저장
    def save_xml_file(self,new_string, code):
        new_root = ET.Element("resources")
        new_root.append(new_string)
        new_tree = ET.ElementTree(new_root)
        new_tree.write(self.output_paths[code], encoding="utf-8", xml_declaration=True)



class LocaleViewer:
    def __init__(self, di_path="", xml_path=""):
        self.di_path=di_path
        self.inputTranslation = InputTranslatrionFile(di_path, xml_path)

    #언어 리스트 가져오기
    def get_country_name(self):
        return self.inputTranslation.load_country()
        