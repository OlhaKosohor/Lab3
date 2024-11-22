from translator.gtranslator import TransLate, LangDetect, LanguageList, CodeLang

if __name__ == "__main__":
    print(TransLate("Hello", "uk"))
    print(CodeLang("fr"))
    detected, confidence = LangDetect("Привіт")
    print(f"Detected lang: {CodeLang(detected)} in probability {confidence}")
    print(LanguageList("Доброго вечора"))
    print("Запис у файл...")
    LanguageList("Доброго ранку", "file")
