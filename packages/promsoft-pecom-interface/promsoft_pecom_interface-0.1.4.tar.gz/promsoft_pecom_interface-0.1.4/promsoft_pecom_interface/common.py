from pydantic import BaseModel


class IdentityCard(BaseModel):
    """
    Документ удостоверяющий личность  [Object]
    """

    type: int = 10  # тип документа [Number]: 10 - ПАСПОРТ ГРАЖДАНИНА РФ, 1 - ПАСПОРТ ИНОСТРАННОГО ГРАЖДАНИНА
    series: str = ""  # Серия [String]
    number: str = ""  # Номер [String]
    date: str = ""  # Дата [DateTime]
