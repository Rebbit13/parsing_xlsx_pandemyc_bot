from models import form_valid_telephone
from .formatted_patient import FormattedPatient


class ContactPatient:
    patient_model = FormattedPatient

    def __init__(self, full_name_and_address: str,
                 birthday: str,
                 telephone_and_occupation: str,
                 status: str):
        self.full_name_and_address = full_name_and_address
        self.telephone_and_occupation = telephone_and_occupation
        self.birthday = birthday
        self.status = status

        self.given_name = None
        self.patronymic = None
        self.surname = None
        self.telephone = None
        self.address = None
        self.occupation = None

    def _parse_full_name_address(self):
        parsed_list = self.full_name_and_address.split(",")
        name_list = parsed_list[0].split()
        if len(name_list) != 3:
            raise ValueError("invalid full_name")
        self.given_name = name_list[1]
        self.patronymic = name_list[2]
        self.surname = name_list[0]
        self.address = ",".join(parsed_list[1:])

    def _parse_telephone_and_occupation(self):
        parsed_list = self.telephone_and_occupation.split("\n")
        if len(parsed_list) == 1:
            parsed_list = self.telephone_and_occupation.split()
        telephone, check = form_valid_telephone(parsed_list[0])
        if check is False:
            self.occupation = self.telephone_and_occupation
        else:
            self.telephone = telephone
            self.occupation = " ".join(parsed_list[1:])

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
        patient = ContactPatient(**patient_dict)
        patient._parse_telephone_and_occupation()
        patient._parse_full_name_address()
        return patient._parse_into_model()
