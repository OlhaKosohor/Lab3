from translator.dtranslator import TransLate, LangDetect, LanguageList, CodeLang

if __name__ == "__main__":
    print(TransLate("Hello", "ja", "en"))
    print(CodeLang("fr"))
    detected, confidence = LangDetect("Hello world")
    print(f"Detected lang {CodeLang(detected)} in prob {confidence}")
    print(LanguageList("Доброго вечора"))
    print("Запис у файл...")
    LanguageList("Доброго ранку", "file")
