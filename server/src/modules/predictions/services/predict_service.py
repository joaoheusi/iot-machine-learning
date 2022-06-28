import keras
from fastapi.encoders import jsonable_encoder
from src.modules.predictions.models.schamas import MachineStatus
from src.shared.providers.pandas.utils import (
    json_to_dataframe,
    ordinal_encoder_categorical_data,
)
from src.shared.providers.scikit_learn.utils import round_predict_score


async def predict_service(machine_status: MachineStatus):
    model = keras.models.load_model("ai_model/model")
    encoded = jsonable_encoder(machine_status.dict())
    df_machine_status = await json_to_dataframe(encoded)
    df_machine_status = await ordinal_encoder_categorical_data(
        data=df_machine_status, drop_first=True
    )
    value = model.predict(df_machine_status)
    value = float(value[0][0] * 100)
    # round value to two decimal digits
    value = await round_predict_score(value)
    return value
