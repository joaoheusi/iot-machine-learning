from typing import List, Optional

from src.modules.predictions.models.documents 


async def fetch_data(skip: int, limit: Optional[int]) -> List[FlightInfoDocument]:
    flights = (
        await FlightInfoDocument.find()
        .project(FlightInfoDocument)
        .skip(skip)
        .limit(limit)
        .to_list()
    )
    return flights