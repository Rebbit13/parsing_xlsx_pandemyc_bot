from datetime import datetime

from documents_helpers import  ExelTableBuilder, XLSXParser


def bot_parse(document_path: str):
    file_name = f"result.xlsx"
    writer = ExelTableBuilder(file_name, sheet_name="12445565",
                              employee="Минина Д.К. врач-эпидемиолог")
    parser = XLSXParser(document_path=document_path,
                        sheet_name="COVID",
                        writer=writer)
    parser.parse()
    return file_name


def parse_from_xlsx():
    time = datetime.now()
    writer = ExelTableBuilder("1234.xlsx", sheet_name="12445565",
                              employee="Минина Д.К. врач-эпидемиолог")
    parser = XLSXParser(document_path="source/Таблица КОВИД (5).xlsx",
                        sheet_name="COVID",
                        writer=writer)
    parser.parse()
    delta = datetime.now() - time
    print(f"Ошибок: {parser.errors}")
    print(f"{delta.seconds} seconds")


if __name__ == '__main__':
    parse_from_xlsx()
