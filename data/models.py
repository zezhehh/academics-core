from pydantic import BaseModel

class Subject(BaseModel):
    id: int | None
    name: str


class Institution(BaseModel):
    id: int | None
    qs_score: float
    times_score: float
    name: str
    lower_case_name: str
    country_code: str
    website: str
