from pydantic import BaseModel


class FormattedPatient(BaseModel):
    given_name: str
    patronymic: str
    surname: str
    address: str = None
    birthday: str = None
    occupation: str = None
    status: str = None
    telephone: int = None
