from typing import Literal
from deep_translator import DeeplTranslator
from langdetect import detect_langs
from .utils import _format_table, _code_lang


def get_deepl(target="en", source="auto", **kwargs):
    return DeeplTranslator(
        source=source,
        target=target,
        api_key="2b530758-2240-4a39-8e94-de3ebc96db3e:fx",
        **kwargs,
    )


LANGUAGES = {v: k for k, v in get_deepl().get_supported_languages(True).items()}


def TransLate(text, dest, scr="auto"):
    try:
        translator = get_deepl(dest, scr)
        translator.source = scr
        translator.target = dest
        result = translator.translate(text)
        return result
    except Exception as e:
        print(e)
        return f"Error: {e}"


def CodeLang(lang):
    return _code_lang(lang, LANGUAGES)


def LangDetect(text: str, set: Literal["all", "lang", "confidence"] = "all"):
    try:
        result = detect_langs(text)
        result = result[0]
        if set == "all":
            return result.lang, result.prob
        elif set == "confidence":
            return result.prob
        elif set == "lang":
            return result.lang
        else:
            raise ValueError("Specify set param")
    except Exception as e:
        return f"Error: {e}"


def LanguageList(text: str, out: str = "screen"):
    detected_input_lang = LangDetect(text, "lang")

    rows = [["N", "Language", "ISO-639 code", "Text"]]
    for idx, lang in enumerate(LANGUAGES):
        rows.append(
            [
                idx + 1,
                LANGUAGES[lang],
                lang,
                TransLate(text, lang, detected_input_lang),
            ]
        )

    if out == "screen":
        for row in _format_table(rows):
            print(row)
    elif out == "file":
        with open("output_deepl.txt", "w", encoding="utf8") as new_file:
            for row in _format_table(rows):
                new_file.write("\n" + row)
            new_file.close()
    else:
        raise ValueError("Incorrect out param")
