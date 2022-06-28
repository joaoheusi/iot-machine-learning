from fastapi import Body, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from src.modules.predictions.models.schamas import MachineStatus, Prediction
from src.modules.predictions.services.predict_service import predict_service

router = APIRouter(
    prefix="/predictions",
    tags=["predictions"],
)


@router.post("/predict", response_model=Prediction)
async def predict(request_body: MachineStatus = Body(...)):
    response = await predict_service(request_body)
    return JSONResponse(
        response.dict(),
        status_code=status.HTTP_200_OK,
    )


""" @router.post("/train_model", response_model=Prediction)
async def train_model(request_body: MachineStatus = Body(...)):
    response = await train_model_service(request_body)
    return JSONResponse(
        response.dict(),
        status_code=status.HTTP_200_OK,
    )
 """
