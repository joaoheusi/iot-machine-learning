from typing import List, Optional

from src.modules.predictions.models.documents import MachineStatus


async def fetch_data(skip: int, limit: Optional[int]) -> List[MachineStatus]:
    machine_statuses = (
        await MachineStatus.find()
        .project(MachineStatus)
        .skip(skip)
        .limit(limit)
        .to_list()
    )
    return machine_statuses
