import numpy
import pandas

from models import FormattedPatient
from . import ExelTableBuilder


class XLSXParser:
    patient_indexes = {"full_name": 4,
                       "birthday": 5,
                       "telephone": 6,
                       "address": 7,
                       "occupation": 8,
                       "status": 19}

    def __init__(self, document_path: str, sheet_name: str, writer: ExelTableBuilder):
        self.errors = 0
        self.document_path = document_path
        self.sheet_name = sheet_name
        self.writer = writer
        self.data_frame: pandas.DataFrame = pandas.read_excel(self.document_path, sheet_name=self.sheet_name)

    @staticmethod
    def _validate_telephone(telephone: str):
        """
        проверка корректности ввода номера телефона
        убирает символы +-()
        :param telephone: введенный пользователем телефон
        :return: кортеж (check - правильно ли введен телефон(bool),
        telephone - если телефон введен корректно отправляет корректный формат 89999999999)
        """
        telephone = str(telephone)
        telephone = telephone.replace("+", "")
        telephone = telephone.replace("-", "")
        telephone = telephone.replace("(", "")
        telephone = telephone.replace(")", "")
        telephone = telephone.replace(" ", "")
        check = False
        if len(telephone) == 11:
            if telephone[0] == "8" or telephone[0] == "7":
                telephone = telephone[1:]
            else:
                raise ValueError("incorrect telephone")
        elif len(telephone) == 10:
            if telephone[0] != "9":
                raise ValueError("incorrect telephone")
        else:
            raise ValueError("incorrect telephone")
        telephone = "8" + telephone
        return int(telephone)

    @staticmethod
    def _parse_name(full_name: str):
        values = full_name.split()
        if len(values) == 3:
            return values
        raise ValueError("wrong fullname")

    def _form_patient(self, index: int):
        patient_dict = {}
        patient_list = self.data_frame.values[index]
        for key, value in self.patient_indexes.items():
            if type(patient_list[value]) == float:
                patient_dict[key] = None
            else:
                patient_dict[key] = patient_list[value]
        try:
            patient_dict["surname"], patient_dict["given_name"], patient_dict["patronymic"] \
                = self._parse_name(patient_dict["full_name"])
        except ValueError:
            print(f"-------------------"
                  f"\nНекорректно заполнено индекс: {index}"
                  f"\nИмя: {patient_dict['full_name']}"
                  f"-------------------")
            self.errors += 1
            return
        except AttributeError:
            print(f"-------------------"
                  f"\nНекорректно заполнено индекс: {index}"
                  f"\nИмя: {patient_dict['full_name']}"
                  f"-------------------")
            self.errors += 1
            return
        if type(patient_dict["birthday"]) == str:
            pass
        elif patient_dict["birthday"]:
            patient_dict["birthday"] = patient_dict["birthday"].strftime("%d.%m.%Y")

        try:
            patient_dict["telephone"] = self._validate_telephone(patient_dict["telephone"])
        except ValueError:
            patient_dict["telephone"] = None
        return FormattedPatient.parse_obj(patient_dict)

    def parse(self):
        i = 0
        while i < int(self.data_frame.index.stop):
            print(i)
            patient = self._form_patient(i)
            if patient:
                self.writer.append(patient)
            i += 1
        self.writer.save_to_file()
