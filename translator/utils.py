def _format_table(array: list[list[str]]):
    col_widths = [max(len(str(item)) for item in column) for column in zip(*array)]
    for row in array:
        yield (
            " ".join(
                f"{str(item).ljust(width)}" for item, width in zip(row, col_widths)
            )
        )


def _code_lang(lang, dictionary):
    for code, language in dictionary.items():
        if language.lower() == lang.lower():
            return code
        elif code.lower() == lang.lower():
            return language
    return None
