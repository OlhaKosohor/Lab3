from googletrans import Translator, LANGUAGES
from googletrans.client import Detected
from .utils import _format_table, _code_lang

translator = Translator()


def TransLate(text, dest, src="auto"):
    try:
        result = translator.translate(text, dest=dest, src=src)
        return result.text
    except Exception as e:
        return f"Error: {e}"


def LangDetect(text: str, set: str = "all"):
    try:
        result: Detected = translator.detect(text)
        if set == "all":
            return result.lang, result.confidence
        elif set == "confidence":
            return result.confidence
        elif set == "lang":
            return result.lang
        else:
            raise ValueError("Specify set param")
    except Exception as e:
        return f"Error: {e}"


def CodeLang(lang):
    return _code_lang(lang, LANGUAGES)


def LanguageList(text: str, out: str = "screen"):

    rows = [["N", "Language", "ISO-639 code", "Text"]]
    for idx, lang in enumerate(LANGUAGES):
        rows.append([idx + 1, LANGUAGES[lang], lang, TransLate(text, lang)])

    if out == "screen":
        for row in _format_table(rows):
            print(row)
    elif out == "file":
        with open("output_google.txt", "w", encoding="utf8") as new_file:
            for row in _format_table(rows):
                new_file.write("\n" + row)
            new_file.close()
    else:
        raise ValueError("Incorrect out param")
