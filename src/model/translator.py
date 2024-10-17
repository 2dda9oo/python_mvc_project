import xml.etree.ElementTree as ET
import os
from model.excel_handler import InputTranslatrionFile

class Translator:

    def __init__(self, di_path="dictionary.xlsx", xml_path="strings.xml", base_dir=""):
        self.di_path = di_path
        self.xml_path = xml_path
        self.base_dir = base_dir
        self.matchedWordList = [] #번역된 name List들
        self.notFoundList = [] #번역안된 name List들
        self.inputTranslation = InputTranslatrionFile(di_path, xml_path)


    def translate_xml(self, input_file):
        output_paths = {}
        excel_dictionary = self.inputTranslation.load_dictionary(self.di_path)
        language_code = list(excel_dictionary[next(iter(excel_dictionary))].keys())
        input_file_name = os.path.basename(input_file)

        self.create_output_directories(language_code, input_file_name, output_paths)

        content_list = [entry['content'] for entry in excel_dictionary]
        tree = ET.parse(input_file)
        root = tree.getroot()

        self.process_xml_strings(root, content_list, excel_dictionary, input_file)

        self.save_xml_files(language_code, output_paths, root)


     #각 언어 코드에 해당하는 디렉토리와 xml 파일 생성
    def create_output_directories(self, language_code, input_file_name, output_paths):
        for code in language_code:
            directory_name = f"values-{code}"
            output_dir = os.path.join(self.base_dir, directory_name)
            os.makedirs(output_dir, exist_ok=True)

            root = ET.Element("resources")
            tree = ET.ElementTree(root)
            output_path = os.path.join(output_dir, input_file_name)
            tree.write(output_path, encoding="utf-8", xml_declaration=True)

            output_paths[code] = output_path

    #번역
    def process_xml_strings(self, root, content_list, excel_dictionary, output_paths, input_file):
        for string_element in root.findall("string"):
            name = string_element.get('name')
            #name이 존재한다면, 번역 데이터 만들기
            if name in content_list:
                translations = excel_dictionary[name]
                for code in translations.keys():
                    translation = translations.get(code)
                    self.matchedWordList.append(name)
                    if translation:
                        new_string = ET.Element("string", name=name)
                        new_string.text = translation

                        self.save_xml_file(new_string, output_paths[code])


            else:
                print(f"{name} is not found in the dictionary.")
                untranslations = excel_dictionary[name]
                for code in untranslations.keys():
                    untranslation = string_element.get(code)
                    self.notFoundList.append(name)
                    if translation:
                        new_string = ET.Element("string", name=name)
                        new_string.text = untranslation
                        self.save_xml_file(new_string, output_paths[code])
            

    #저장
    def save_xml_file(self,new_string, output_path):
        new_root = ET.Element("resources")
        new_root.append(new_string)
        new_tree = ET.ElementTree(new_root)
        new_tree.write(output_path, encoding="utf-8", xml_declaration=True)
    

class LocaleViewer:
    def __init__(self, di_path="", xml_path=""):
        self.di_path=di_path
        self.inputTranslation = InputTranslatrionFile(di_path, xml_path)

    #언어 리스트 가져오기
    def get_country_name(self):
        return self.inputTranslation.load_country()
        