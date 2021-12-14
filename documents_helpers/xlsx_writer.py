import pandas

from models import FormattedPatient


class ExelTableBuilder:
    index = 1
    indexes = []
    table = {
        "№ п/п": [],
        "Номер экстренного извещения": [],
        "Дата экстренного извещения": [],
        "Дата получения экстренного извещения": [],
        "Фамилия": [],
        "Имя": [],
        "Отчество": [],
        "Дата рождения": [],
        "Место работы": [],
        "Профессия": [],
        "Адрес фактического проживания": [],
        "Дата последнего контакта с больным COVID": [],
        "Дата окончания медицинского наблюдения": [],
        "Причина соблюдения режима изоляции": [],
        "Гражданская принадлежность": [],
        "ФИО законного представителя ребёнка, дата рождения": [],
        "Сотовый телефон": [],
        "Адрес электронной почты": [],
        "Способ информирования гражданина": [],
        "время и дата информирования гражданина": [],
        "ФИО специалиста": [],
    }

    def __init__(self, document_path: str, sheet_name: str,
                 employee: str = "Меркулова С.В.помощник врача-эпидемиолога"):
        self.writer = pandas.ExcelWriter(document_path, engine='xlsxwriter')
        self.sheet_name = sheet_name
        self.employee = employee

    def append(self, patient: FormattedPatient):
        self.table["№ п/п"].append(self.index)
        self.indexes.append(self.index)
        self.index += 1
        self.table["Номер экстренного извещения"].append("")
        self.table["Дата экстренного извещения"].append("")
        self.table["Дата получения экстренного извещения"].append("")
        self.table["Фамилия"].append(patient.surname)
        self.table["Имя"].append(patient.given_name)
        self.table["Отчество"].append(patient.patronymic)
        self.table["Дата рождения"].append(patient.birthday)
        self.table["Место работы"].append(patient.occupation)
        self.table["Профессия"].append(patient.occupation)
        self.table["Адрес фактического проживания"].append(patient.address)
        self.table["Дата последнего контакта с больным COVID"].append("")
        self.table["Дата окончания медицинского наблюдения"].append("")
        self.table["Причина соблюдения режима изоляции"].append("")
        self.table["Гражданская принадлежность"].append("Российская Федерация")
        self.table["ФИО законного представителя ребёнка, дата рождения"].append("")
        self.table["Сотовый телефон"].append(patient.telephone)
        self.table["Адрес электронной почты"].append("")
        self.table["Способ информирования гражданина"].append("по телефону")
        self.table["время и дата информирования гражданина"].append("")
        self.table["ФИО специалиста"].append(self.employee)

    def save_to_file(self):
        dataframe = pandas.DataFrame(self.table, self.indexes)
        dataframe.to_excel(self.writer, startrow=2)
        self.writer.save()
