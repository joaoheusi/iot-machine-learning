from ast import operator
from pydantic import BaseModel


class Prediction(BaseModel):
    prediction: bool


class MachineStatus(BaseModel):
    date: str
    temperature: float
    humidity: float
    operator: str
    measure1: float
    measure2: str
    measure3: str
    measure4: float
    measure5: float
    measure6: float
    measure7: float
    measure8: float
    measure9: float
    measure10: float
    measure11: float
    measure12: float
    measure13: float
    measure14: float
    measure15: float
    hours_since_previous_failure: float
    failure: bool
    date_year: int
    date_month: int
    date_day: int
    date_hour: int
    date_minute: int
    date_second: int
    date_day_of_week: str
