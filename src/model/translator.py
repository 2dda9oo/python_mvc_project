import xml.etree.ElementTree as ET
import os
from model.excel_handler import InputTranslatrionFile
from .excel_handler import language_code
import re



class Translator:

    def __init__(self, di_path="dictionary.xlsx", xml_path="strings.xml", base_dir=""):
        
        self.di_path = di_path
        self.xml_path = xml_path
        self.base_dir = base_dir

        self.inputTranslation = InputTranslatrionFile(di_path, xml_path) #excel_handler 초기화
        self.matched_word_list = [] #번역된 text List들
        self.not_found_list = {} #번역안된 text dict(key-value:name-text)
        self.output_paths = {}
        self.content_list = []

        self.not_need_check_dict = {} #체크가 필요없는 dict(key-value:name-text)
        self.formatted_translation_content_dict = {} # name: {formattedText, text}-2단계 번역시 사용
        self.formatted_text_dict = {} # 형식 name: {formattedText, text}-2단계 번역시 사용
        self.need_check_dict = {} #체크가 필요한 text dict Name: {'check_text': 'Name', 'check_translation_text': 'name'}
        self.excel_dictionary = {}

        self.translated_name = None
        self.transalted_text = None


    #string.xml 번역 실행
    def translate_xml(self):

        self.excel_dictionary = self.inputTranslation.load_dictionary() #excel 핸들러 통해 translation dictionary 획득
        self.content_list = list(self.excel_dictionary.keys()) #dictionary의 key 통해 English Text 획득
        language_code = list(self.excel_dictionary[next(iter(self.excel_dictionary))].keys()) #dictionary의 values 통해 국가 코드 List 획득

        input_file_name = os.path.basename(self.xml_path) #xml 파일의 이름 string
        self.create_output_directories(language_code, input_file_name) #번역 결과 xml 파일 저장할 directory 생성 메서드 호출
        tree = ET.parse(self.xml_path)
        root = tree.getroot()

        print("Translation START!")

        #1단계 번역 시작
        self.process_xml_strings(root)
        print("1nd Translation completed.")

        #2단계 번역 시작
        self.prepare_formatted_data()
        self.checkTranslate()
        print("2nd Translation completed.")

        #3단계 번역 시작
        self.translateMissMatched()
        print("3nd Translation completed.")


    #번역 파일과 매칭된 string들의 List 반환
    def getMatchedList(self):
        return self.matched_word_list
    
    
    #번역 파일과 매칭되지 않은 String들의 List 반환
    def getNotFoundList(self):
        value_list = list(self.not_found_list.values())
        return value_list
    
    
    #번역 파일과 매칭되지 않은 String들 txt 파일로 저장
    def save_txt_file(self, list):
        with open('output.txt', 'w', encoding='utf-8') as f:
            for item in list:
                f.write(f"{item}\n")
        print("Save txt file")


    #string.xml의 name 획득
    def getTranslatedName(self):
        return self.translated_name
    
    
    #string.xml의 text content 획득
    def getTranslatedText(self):
        return self.transalted_text


    #xml 파일 저장 - 중복되는 elements(name)는 덮어쓰기
    def save_xml_file(self, new_string, code):
        tree = ET.parse(self.output_paths[code])
        root = tree.getroot()
        modified_element = root.find(f"./string[@name='{new_string.attrib['name']}']")
        if modified_element is not None:
            modified_element.text = new_string.text
        else:
            root.append(new_string)

        self.indent(root)

        tree.write(self.output_paths[code], encoding="utf-8", xml_declaration=True)


    #elements들간 줄바꿈 적용
    def indent(self, elem, level=0):
        i = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for subelem in elem:
                self.indent(subelem, level + 1)
            if not subelem.tail or not subelem.tail.strip():
                subelem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i


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


    #1단계 번역 - 기본 매칭
    def process_xml_strings(self, root):
        for string_element in root.findall("string"):
            name = string_element.get('name')
            text = string_element.text #코드 주의
            #translation_file에 text가 존재한다면, 언어 별로 번역하기
            if text in self.content_list:
                translations = self.excel_dictionary[text]

                for code in language_code:
                    translation = translations.get(code)

                    if translation:
                        new_string = ET.Element("string", name=name)
                        new_string.text = translation
                        self.save_xml_file(new_string, code)
                self.matched_word_list.append(text)

            else:                
                for code in language_code:
                    new_string = ET.Element("string", name=name)
                    new_string.text = text
                    self.save_xml_file(new_string, code)

                self.not_found_list[name]=text


    #2단계 번역 - Need Checking(대소문자, 공백 구분)
    def prepare_formatted_data(self):
        for name, not_found_text in self.not_found_list.items():
            formatted_text = not_found_text.replace(" ","").upper()
            self.formatted_text_dict[name] = {
                'text': not_found_text,
                'formatted_text': formatted_text
            }
        for content in self.content_list:
            content_str = str(content) if content is not None else ""
            formatted_content = content_str.replace(" ","").upper()
            self.formatted_translation_content_dict[content] = formatted_content

    def find_keys_by_formatted_text(self, target_formatted_text):
        for key, value in self.formatted_translation_content_dict.items():
            if value == target_formatted_text:
                return key

    def checkTranslate(self):
        for name in self.formatted_text_dict.keys():
            formatted_text = self.formatted_text_dict[name]['formatted_text']
            #해당name이 translation에 있는지 확인 -> 있으면 need_check_dict에 추가
            if formatted_text in self.formatted_translation_content_dict.values():
                name = name
                check_text = self.formatted_text_dict[name]['text']
                check_translation_text = self.find_keys_by_formatted_text(formatted_text)
                self.need_check_dict[name] = {
                'check_text': check_text,
                'check_translation_text': check_translation_text
            }
            #없으면 not_need_check_dict에 추가
            else: 
                self.not_need_check_dict[name]=self.formatted_text_dict[name]['text']
    
    

    #3단계 번역 - 특수기호 구분
    def translateMissMatched(self):
        for name, text in self.not_need_check_dict.items():
            split_chars = r'[\n\(\)\-\!\$]'
            splited_list = re.split(split_chars, text)
            splited_list = list(filter(None, splited_list))
            
            is_in = False

            for splitedItem in splited_list:
                if splitedItem in self.content_list:
                    is_in = True
                else:
                    is_in = False
                    break

            if is_in:
                self.not_found_list.pop(name, None)
                self.matched_word_list.append(text)

                for code in language_code:
                    name_content = text
                    for splitedItem in splited_list:
                        translations = self.excel_dictionary[splitedItem]
                        translation = translations.get(code)
                        name_content = name_content.replace(splitedItem, translation, 1)
                    new_string = ET.Element("string", name=name)
                    new_string.text = name_content
                    self.save_xml_file(new_string, code)
             

    #translate버튼 함수(need_check TableView 버튼 클릭된 경우, xml번역 실행)
    def need_check_translate_btn(self,index):
        check_translation_text = None
        check_text = None
        values = list(self.need_check_dict.values())
        name = list(self.need_check_dict.keys())[index]
        if 0 <= index < len(values):
            check_translation_text = values[index]['check_translation_text']
            check_text = values[index]['check_text']
            translations = self.excel_dictionary[check_translation_text]

            for code in language_code:
                translation = translations.get(code)
            
                new_string = ET.Element("string", name=name)
                new_string.text = translation

                self.save_xml_file(new_string, code)

            self.matched_word_list.append(name)
            self.not_found_list.pop(name)
            self.need_check_dict.pop(name)

            self.translated_name = name
            self.transalted_text = check_text           
            
        else:
            raise IndexError("error")
    