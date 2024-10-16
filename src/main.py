from controller.translator_controller import TranslatorController

def main():
    controller = TranslatorController()
    input_file = input("파일 입력이 필요함.")
    controller.translate(input_file)

if __name__ == "__main__":
    main()

