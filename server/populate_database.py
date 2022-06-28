import asyncio
import json
import random
from datetime import datetime
from typing import Any, Dict, List

from beanie import init_beanie
from config import MONGODB_URL
from motor.motor_asyncio import AsyncIOMotorClient
from src.modules.predictions.models.documents import MachineStatus


def str_to_datestr(string_date: str) -> str:
    new_datetime = datetime.strptime(string_date, "%d-%m-%Y")
    new_date = new_datetime.date()
    return str(new_date)


def str_to_bool(string_bool: str) -> bool:
    if string_bool == "No" or string_bool == "False":
        return False
    return True


async def populate_database_from_json():
    with open("machine_failures.json", "r", encoding="utf-8") as f:
        raw = f.read()

    data: List[Dict] = json.loads(raw)
    for item in data:
        new_machine_status = MachineStatus(
            date=item["Date"],
            temperature=item["Temperature"],
            humidity=item["Humidity"],
            operator=item["Operator"],
            measure1=item["Measure1"],
            measure2=item["Measure2"],
            measure3=item["Measure3"],
            measure4=item["Measure4"],
            measure5=item["Measure5"],
            measure6=item["Measure6"],
            measure7=item["Measure7"],
            measure8=item["Measure8"],
            measure9=item["Measure9"],
            measure10=item["Measure10"],
            measure11=item["Measure11"],
            measure12=item["Measure12"],
            measure13=item["Measure13"],
            measure14=item["Measure14"],
            measure15=item["Measure15"],
            hours_since_previous_failure=item["Hours_Since_Previous_Failure"],
            failure=item["Failure"],
            date_year=item["Date_year"],
            date_month=item["Date_month"],
            date_day_of_week=item["Date_day-of-week"],
            date_day=item["Date_day-of-month"],
            date_hour=item["Date_hour"],
            date_minute=item["Date_minute"],
            date_second=item["Date_second"],
        )
        await new_machine_status.insert()


DOCUMENT_MODELS_POPULATE = [MachineStatus]


async def main():
    database = AsyncIOMotorClient(MONGODB_URL).iotapplication
    await init_beanie(database, document_models=DOCUMENT_MODELS_POPULATE)
    await populate_database_from_json()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
