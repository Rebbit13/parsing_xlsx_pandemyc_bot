from .formatted_patient import FormattedPatient
from .utils import form_valid_telephone


class Patient:
    patient_model = FormattedPatient

    def __init__(self, full_name: str,
                 telephone_and_result: str,
                 address: str,
                 birthday: str,
                 occupation: str,
                 status: str):
        self.full_name = full_name
        self.telephone_and_result = telephone_and_result
        self.address = address
        self.birthday = birthday
        self.occupation = occupation
        self.status = status
        self.given_name = None
        self.patronymic = None
        self.surname = None
        self.telephone = None

    def _parse_full_name(self):
        name_list = self.full_name.split()
        if len(name_list) != 3:
            raise ValueError("invalid full_name")
        self.given_name = name_list[1]
        self.patronymic = name_list[2]
        self.surname = name_list[0]

    def _parse_telephone(self):
        parsed_list = self.telephone_and_result.split("\n")
        if len(parsed_list) == 1:
            parsed_list = self.telephone_and_result.split()
        telephone, check = form_valid_telephone(parsed_list[0])
        if check is False:
            raise ValueError("invalid telephone")
        self.telephone = telephone

    def _parse_into_model(self):
        return self.patient_model(given_name=self.given_name,
                                  patronymic=self.patronymic,
                                  surname=self.surname,
                                  address=self.address,
                                  birthday=self.birthday,
                                  occupation=self.occupation,
                                  status=self.status,
                                  telephone=self.telephone)

    @staticmethod
    def form(patient_dict: dict):
        patient = Patient(**patient_dict)
        patient._parse_telephone()
        patient._parse_full_name()
        return patient._parse_into_model()
