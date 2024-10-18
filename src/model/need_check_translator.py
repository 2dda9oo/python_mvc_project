class Need_check_Translator:
        
    def __init_(self,not_found_list,content_list):
        self.not_found_list = not_found_lsit #1차 번역 안 된 리스트들
        self.formatted_translation_content_dict = [] # formattedContent-content -> 나중에 content로 translation_file에서 각 언어 번역 찾아야함.
        self.formatted_name_dict = [] #formattentName-name
        self.need_check_dict = []
        self.not_need_check_dict = [] #dict할지 고민 중
        self.content_list = content_list

        self.prepare_formatted_data(content_list)

    def prepare_formatted_data(self, content_list):
        for not_found_name in not_found_list:
            formatted_name = not_found_name.replace(" ","").upper()
            self.formatted_name_dict.append(formatted_name)
            #formatted_name을 리스트로..? 아니면 dict로?
        for content in content_list:
            formatted_content = content.replace(" ","").upper()
            self.formatted_translation_content_dict[formatted_content] = content

    def checkTranslate(self):
        for  formatted_name in self.formatted_name_dict: #name
            if formatted_name in self.formatted_translation_content_dict: #해당name이 translation에 있는지 확인 -> 있으면 need_check_dict에 추가
                self.need_check_dict[formatted_name] = self.formatted_translation_content_dict[formatted_name] #name - content
                #리스트에 보여주기!!!!!!
                #event click Listender로! convert 버튼 누르면, string 파일 작성되고 not_ok_list에서 삭제되기

            else: #없으면 not_need_check_dict에 name 리스트만 append
                self.not_need_check_dict.append(formatted_name_dict[name])





