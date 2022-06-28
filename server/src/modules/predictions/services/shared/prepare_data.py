from typing import List

from fastapi.encoders import jsonable_encoder
from src.modules.predictions.models.documents import MachineStatus


async def prepare_data(data: List[MachineStatus]) -> List[MachineStatus]:
    prepared_data = data

    return prepared_data
