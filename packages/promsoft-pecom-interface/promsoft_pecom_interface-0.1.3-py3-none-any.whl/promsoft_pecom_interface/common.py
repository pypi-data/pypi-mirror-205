from pydantic import BaseModel


class IdentityCard(BaseModel):
    """
    Документ удостоверяющий личность  [Object]
    """

    type: str = ""  # ПАСПОРТ ГРАЖДАНИНА РФ ИЛИ ИНОСТРАННЫЙ (passport| passport_foreign)
    series: str = ""  # Серия [String]
    number: str = ""  # Номер [String]
    date: str = ""  # Дата [DateTime]
