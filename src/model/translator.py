import xml.etree.ElementTree as ET
import os
from model.excel_handler import InputTranslatrionFile
import json
from .excel_handler import language_code
import re


class Translator:

    def __init__(self, di_path="dictionary.xlsx", xml_path="strings.xml", base_dir=""):
        self.di_path = di_path
        self.xml_path = xml_path
        self.base_dir = base_dir
        self.matchedWordList = [] #번역된 name List들
        self.notFoundList = {} #번역안된 text List(name-text쌍으로)
        self.output_paths = {}
        self.inputTranslation = InputTranslatrionFile(di_path, xml_path)
        self.content_list = []

    def translate_xml(self):
        excel_dictionary = self.inputTranslation.load_dictionary()
        # 처음 5개의 키와 값 출력
        for i, (key, value) in enumerate(excel_dictionary.items()):
            if i < 5:  # 처음 5개 항목만 출력
                print(f"Key: {key}, Value: {value}")
            else:
                break

        language_code = list(excel_dictionary[next(iter(excel_dictionary))].keys())
        input_file_name = os.path.basename(self.xml_path)
        self.create_output_directories(language_code, input_file_name)
        self.content_list = list(excel_dictionary.keys())
        tree = ET.parse(self.xml_path)
        root = tree.getroot()

        self.process_xml_strings(root, excel_dictionary)
        

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
    def process_xml_strings(self, root, excel_dictionary):
        for string_element in root.findall("string"):
            name = string_element.get('name')
            text = string_element.text #코드 주의
            print(f"Element: {ET.tostring(string_element, encoding='unicode')}")
            print("text: "+str(text))
            #name이 존재한다면, 번역 데이터 만들기
            if text in self.content_list: #name->text수정
                translations = excel_dictionary[text]
                print("translations: " + json.dumps(translations))  # 딕셔너리 출력
                for code in language_code:
                    translation = translations.get(code)
                    print("code-translation: " + code)
                    print("translation: " + str(translation))  # translation을 문자열로 변환
                    if translation:
                        new_string = ET.Element("string", name=name)
                        new_string.text = translation

                        self.save_xml_file(new_string, code)
                self.matchedWordList.append(text)


            else:
                print("Content List:", self.content_list)

                print(f"{text} is not found in the dictionary.")
                
                for code in language_code:
                    new_string = ET.Element("string", name=name)
                    new_string.text = text
                    self.save_xml_file(new_string, code)

                self.notFoundList[name]=text


    def save_xml_file(self, new_string, code):
        tree = ET.parse(self.output_paths[code])
        root = tree.getroot()
        root.append(new_string)
        tree.write(self.output_paths[code], encoding="utf-8", xml_declaration=True)


    def getMatchedWordList(self):
        print("Matched Word List:", self.matchedWordList)
        return self.matchedWordList
    
    def getNotFoundList(self):
        return self.notFoundList
    
    def translateMissMatched(self, content_list, excel_dictionary):
        print("Not Found List:", self.notFoundList)
        for text in self.notFoundList:
            split_chars = r'[\n\(\)\-\!\$]'
            splited_list = re.split(split_chars, text)
            splited_list = list(filter(None, splited_list))
            print("split content check:", splited_list)
            is_in = True

            for splitedItem in splited_list:
                if splitedItem in content_list:
                    is_in = True
                else:
                    is_in = False
                    break

            if is_in:
                self.notFoundList.remove(text)
                self.matchedWordList.append(text)

                for code in language_code:
                    name_content = text
                    for splitedItem in splited_list:
                        translations = excel_dictionary[splitedItem]
                        translation = translations.get(code)
                        name_content = name_content.replace(splitedItem, translation, 1)
                        print("translation:", translation)
                    new_string = ET.Element("string")
                    new_string.text = name_content
                    print("replace file content: " + ET.tostring(new_string, encoding='unicode'))
                    self.save_xml_file(new_string, code)
        


class LocaleViewer:
    def __init__(self, di_path="", xml_path=""):
        self.di_path=di_path
        self.inputTranslation = InputTranslatrionFile(di_path, xml_path)

    #언어 리스트 가져오기
    def get_country_name(self):
        return self.inputTranslation.load_country()
