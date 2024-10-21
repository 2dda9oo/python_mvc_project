class Need_check_Translator:
        
    def __init__(self,not_found_list,content_list):
        self.not_found_list = not_found_list #1차 번역 안 된 리스트의 dictionary(name-text형태)
        self.formatted_translation_content_dict = {} # name: {formattedText, text}-> 나중에 content로 translation_file에서 각 언어 번역 찾아야함.
        self.formatted_text_dict = {} # name: {formattedText, text}
        self.need_check_dict = {} #체크가 필요한 리스트들 Name: {'check_text': 'Name', 'check_translation_text': 'name'}
        self.not_need_check_dict = {} #체크가 필요없는 리스트들(key-value:name-text)
        self.content_list = content_list

        #not_found_list출력 체크
        print("not_found_list: " + ', '.join(self.not_found_list.values()))

        self.prepare_formatted_data(content_list)



    def prepare_formatted_data(self, content_list):
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
        for content in content_list:
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

    






