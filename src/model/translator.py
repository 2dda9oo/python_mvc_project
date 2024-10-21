import xml.etree.ElementTree as ET
import os
from model.excel_handler import InputTranslatrionFile
from .excel_handler import language_code
import re
import json
import re


class Translator:

    def __init__(self, di_path="dictionary.xlsx", xml_path="strings.xml", base_dir=""):
        self.di_path = di_path
        self.xml_path = xml_path
        self.base_dir = base_dir
        self.matched_word_list = [] #번역된 name List들
        self.not_found_list = {} #번역안된 text List(name-text쌍으로)
        self.output_paths = {}
        self.inputTranslation = InputTranslatrionFile(di_path, xml_path)
        self.content_list = []

        self.not_need_check_dict = {} #체크가 필요없는 리스트들(key-value:name-text)
        self.formatted_translation_content_dict = {} # name: {formattedText, text}-> 나중에 content로 translation_file에서 각 언어 번역 찾아야함.
        self.formatted_text_dict = {} # name: {formattedText, text}
        self.need_check_dict = {} #체크가 필요한 리스트들 Name: {'check_text': 'Name', 'check_translation_text': 'name'}


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
        #1단계 번역 시작
        self.process_xml_strings(root, excel_dictionary)
        print("1nd Translation completed.")
        #2단계 번역 시작
        self.prepare_formatted_data()
        self.checkTranslate()
        print("2nd Translation completed.")

        #3단계 번역 시작
        self.translateMissMatched(excel_dictionary)
        print("3nd Translation completed.")

        return self.need_check_dict
    
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
                self.matched_word_list.append(text)

            else:
                print("Content List:", self.content_list)

                print(f"{text} is not found in the dictionary.")

                
                for code in language_code:
                    new_string = ET.Element("string", name=name)
                    new_string.text = text
                    self.save_xml_file(new_string, code)

                self.not_found_list[name]=text


    def save_xml_file(self, new_string, code):
        tree = ET.parse(self.output_paths[code])
        root = tree.getroot()
        root.append(new_string)
        tree.write(self.output_paths[code], encoding="utf-8", xml_declaration=True)


    #Second Stage Translate
    def prepare_formatted_data(self):
        for name, not_found_text in self.not_found_list.items():
            formatted_text = not_found_text.replace(" ","").upper()
            self.formatted_text_dict[name] = {
                'text': not_found_text,
                'formatted_text': formatted_text
            }
            #self.formatted_text_dict[formatted_text]=not_found_text
        #formatted_text_dict 확인
        formatted_items = "\n".join([f"{key}: {value}" for key, value in self.formatted_text_dict.items()])
        print("formatted_text - not_found_text:\n" + formatted_items)
        for content in self.content_list:
            content_str = str(content) if content is not None else ""
            formatted_content = content_str.replace(" ","").upper()
            self.formatted_translation_content_dict[content] = formatted_content
            # self.formatted_translation_content_dict[formatted_content] = content
        #formatted_translation_dict 확인
        formatted_translations = "\n".join([f"{key}: {value}" for key, value in self.formatted_translation_content_dict.items()])
        print("formatted_content - content:\n" + formatted_translations)

    def find_keys_by_formatted_text(self, target_formatted_text):
        for key, value in self.formatted_translation_content_dict.items():
            if value == target_formatted_text:
                return key

    def checkTranslate(self):
        for name in self.formatted_text_dict.keys(): #name
            formatted_text = self.formatted_text_dict[name]['formatted_text']
            if formatted_text in self.formatted_translation_content_dict.values(): #해당name이 translation에 있는지 확인 -> 있으면 need_check_dict에 추가
                name = name
                check_text = self.formatted_text_dict[name]['text']
                check_translation_text = self.find_keys_by_formatted_text(formatted_text)
                self.need_check_dict[name] = {
                'check_text': check_text,
                'check_translation_text': check_translation_text
            }
                print(f"Check needed for: {check_text}")
                #리스트에 보여주기!!!!!!
                #event click Listender로! convert 버튼 누르면, string 파일 작성되고 not_ok_list에서 삭제되기

            else: #없으면 not_need_check_dict에 name 리스트만 
                print(f"No check needed for: {self.formatted_text_dict[name]['text']}")
                self.not_need_check_dict[name]=self.formatted_text_dict[name]['text'] #이건 다시 특수문자있는지 확인하면서 3단계 번역으로 넘어가기

        Need_check = "\n".join([f"{key}: {value}" for key, value in self.need_check_dict.items()])
        print("NEED\nname - content:\n" + Need_check)

        Need_check = "\n".join([f"{key}: {value}" for key, value in self.not_need_check_dict.items()])
        print("NOT NEED\nformatted_content - content:\n" + Need_check)
    

    #특수기호 구분 번역
    def translateMissMatched(self, excel_dictionary):

        text_list = list(self.not_need_check_dict.values())
        print("Not Found List:", text_list)
        for name, text in self.not_need_check_dict.items():
            split_chars = r'[\n\(\)\-\!\$]'
            splited_list = re.split(split_chars, text)
            splited_list = list(filter(None, splited_list))
            print("split content check:", splited_list)
            is_in = False

            for splitedItem in splited_list:
                if splitedItem in self.content_list:
                    is_in = True
                else:
                    is_in = False
                    break

            if is_in:
                self.not_found_list.pop(text, None)
                self.matched_word_list.append(text)

                for code in language_code:
                    name_content = text
                    for splitedItem in splited_list:
                        translations = excel_dictionary[splitedItem]
                        translation = translations.get(code)
                        name_content = name_content.replace(splitedItem, translation, 1)
                        print("translation:", translation)
                    new_string = ET.Element("string", name=name)
                    new_string.text = name_content
                    print("replace file content: " + ET.tostring(new_string, encoding='unicode'))
                    self.save_xml_file(new_string, code)

