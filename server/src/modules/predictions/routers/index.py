from typing import Optional

from fastapi import Body, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from src.modules.predictions.models.schamas import MachineStatus, Prediction
from src.modules.predictions.services.predict_service import predict_service
from src.modules.predictions.services.train_model_service import train_model_service

router = APIRouter(
    prefix="/predictions",
    tags=["predictions"],
)


@router.post("/predict", response_model=Prediction)
async def predict(request_body: MachineStatus = Body(...)):
    response = await predict_service(request_body)
    return JSONResponse(
        {"chance_of_failure_percentage": response},
        status_code=status.HTTP_200_OK,
    )


@router.post("/train_model")
async def train_model(skip: int = 0, limit: Optional[int] = None):
    response = await train_model_service(skip=skip, limit=limit)
    return JSONResponse(
        response,
        status_code=status.HTTP_200_OK,
    )
