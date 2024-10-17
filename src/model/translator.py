import xml.etree.ElementTree as ET
import os
<<<<<<< HEAD
from model.excel_handler import InputTranslatrionFile
=======
import model.excel_handler as EH
from .excel_handler import language_code
>>>>>>> 0df1dde (translator code updating(mapping error 해결 중))

class Translator:

    def __init__(self, di_path="dictionary.xlsx", xml_path="strings.xml", base_dir=""):
        self.di_path = di_path
        self.xml_path = xml_path
        self.base_dir = base_dir
<<<<<<< HEAD
        self.matchedWordList = [] #번역된 name List들
        self.notFoundList = [] #번역안된 name List들
        self.inputTranslation = InputTranslatrionFile(di_path, xml_path)


    def translate_xml(self, input_file):
        output_paths = {}
        excel_dictionary = self.inputTranslation.load_dictionary(self.di_path)
=======
        self.matchedWordList = []  # 번역된 name 리스트
        self.notFoundList = []  # 번역되지 않은 name 리스트
        self.output_paths = {}  # 각 언어 코드에 대한 경로 저장

    def translate_xml(self):
        excel_dictionary = EH.load_dictionary(self.di_path)
        
        # 언어 코드 리스트 추출
>>>>>>> 0df1dde (translator code updating(mapping error 해결 중))
        language_code = list(excel_dictionary[next(iter(excel_dictionary))].keys())
        input_file_name = os.path.basename(self.xml_path)
        
        # 언어별로 디렉토리 생성 및 파일 경로 준비
        self.create_output_directories(language_code, input_file_name)

        content_list = list(excel_dictionary.keys())

        # 원본 XML 파일 로드
        tree = ET.parse(self.xml_path)
        root = tree.getroot()

        # 번역 처리
        self.process_xml_strings(root, content_list, excel_dictionary)

    # 각 언어 코드에 해당하는 디렉토리와 xml 파일 생성
    def create_output_directories(self, language_code, input_file_name):
        for code in language_code:
            directory_name = f"values-{code}"
            output_dir = os.path.join(self.base_dir, directory_name)
            os.makedirs(output_dir, exist_ok=True)

            # 언어별로 새로운 XML 파일 생성 준비
            output_path = os.path.join(output_dir, input_file_name)
            self.output_paths[code] = output_path

    # 번역
    def process_xml_strings(self, root, content_list, excel_dictionary):
        for string_element in root.findall("string"):
            name = string_element.get('name')
            original_text = string_element.text  # 원본 텍스트
            
            # name이 존재하면 번역 작업 진행
            if name in content_list:
                print("name,content_list:"+name+"/"+content_list)
                translations = excel_dictionary[name]
                for code in language_code:
                    translation = translations.get(code)
                    if translation:
                        new_string = ET.Element("string", name=name)
                        new_string.text = translation
                        
                        # 번역된 string 요소를 해당 언어 파일에 추가
                        self.save_xml_file(new_string, code)
                        self.matchedWordList.append(name)
            else:
                # 번역할 수 없는 경우 원본 텍스트 추가
                for code in language_code:
                    new_string = ET.Element("string", name=name)
                    new_string.text = original_text
                    self.save_xml_file(new_string, code)
                    self.notFoundList.append(name)

    # 저장: 각 언어별로 해당하는 XML 파일에 string 요소 추가
    def save_xml_file(self, new_string, code):
        output_path = self.output_paths[code]

        # 기존 파일이 존재하면 로드, 없으면 새로 생성
        if os.path.exists(output_path):
            tree = ET.parse(output_path)
            root = tree.getroot()
        else:
            root = ET.Element("resources")
            tree = ET.ElementTree(root)

        # 새로운 string 요소 추가
        root.append(new_string)

<<<<<<< HEAD
    #저장
    def save_xml_file(self,new_string, output_path):
        new_root = ET.Element("resources")
        new_root.append(new_string)
        new_tree = ET.ElementTree(new_root)
        new_tree.write(output_path, encoding="utf-8", xml_declaration=True)
    
=======
        # 파일에 다시 쓰기 (덮어쓰기)
        tree.write(output_path, encoding="utf-8", xml_declaration=True)
>>>>>>> 0df1dde (translator code updating(mapping error 해결 중))

class LocaleViewer:
    def __init__(self, di_path="", xml_path=""):
        self.di_path=di_path
        self.inputTranslation = InputTranslatrionFile(di_path, xml_path)

    #언어 리스트 가져오기
    def get_country_name(self):
        return self.inputTranslation.load_country()
        