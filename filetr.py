import os
import re
import json
from pathlib import Path
from translator.gtranslator import TransLate, LangDetect


def get_file_stats(file_path):
    try:
        file_stats = os.stat(file_path)
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()

        num_chars = len(text)
        num_words = len(text.split())
        num_sentences = len(re.split(r"[.!?]", text)) - 1
        file_size = file_stats.st_size

        return {
            "file_size": file_size,
            "num_chars": num_chars,
            "num_words": num_words,
            "num_sentences": num_sentences,
            "language": LangDetect(text, "lang"),
        }
    except FileNotFoundError:
        return {"error": "File not found"}
    except Exception as e:
        return {"error": str(e)}


def read_config(config_file):
    try:
        with open(config_file, "r", encoding="utf-8") as file:
            config = json.load(file)
        return config
    except FileNotFoundError:
        return {"error": "Config file not found"}
    except json.JSONDecodeError:
        return {"error": "Error decoding config file"}
    except Exception as e:
        return {"error": str(e)}


def main():
    config = read_config("config.json")

    if "error" in config:
        print(config["error"])
        return

    input_file = config.get("input_file")
    if not input_file:
        print("Input file not specified in the config.")
        return

    file_stats = get_file_stats(input_file)

    if "error" in file_stats:
        print(file_stats["error"])
        return

    print(f"File name: {input_file}")
    print(f"File size: {file_stats['file_size']} bytes")
    print(f"Number of characters: {file_stats['num_chars']}")
    print(f"Number of words: {file_stats['num_words']}")
    print(f"Number of sentences: {file_stats['num_sentences']}")
    print(f"Language: {file_stats['language']}")

    text_limit = {
        "char_limit": config.get("char_limit", float("inf")),
        "word_limit": config.get("word_limit", float("inf")),
        "sentence_limit": config.get("sentence_limit", float("inf")),
    }

    with open(input_file, "r", encoding="utf-8") as file:
        text = ""
        for line in file:
            text += line
            if (
                len(text) > text_limit["char_limit"]
                or len(text.split()) > text_limit["word_limit"]
                or len(re.split(r"[.!?]", text)) - 1 > text_limit["sentence_limit"]
            ):
                break

    target_language = config.get("target_language")
    if not target_language:
        print("Target language not specified in the config.")
        return

    translated_text = TransLate(text, target_language)

    if "error" in translated_text:
        print(translated_text["error"])
        return

    output_method = config.get("output_method", "screen")
    if output_method == "screen":
        print(f"Translated language: {target_language}")
        print(f"Translated text: {translated_text}")
    elif output_method == "file":
        output_file = f"{Path(input_file).stem}_{target_language}.txt"
        try:
            with open(output_file, "w", encoding="utf-8") as file:
                file.write(translated_text)
            print("Ok")
        except Exception as e:
            print(f"Error writing to file: {str(e)}")
    else:
        print("Invalid output method specified in the config.")


if __name__ == "__main__":
    main()
