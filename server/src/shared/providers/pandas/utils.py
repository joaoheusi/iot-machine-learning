from typing import List

from fastapi.encoders import jsonable_encoder
from pandas import DataFrame, get_dummies, json_normalize
from sklearn.preprocessing import OrdinalEncoder
from src.modules.predictions.models.documents import MachineStatus


async def json_to_dataframe(prepared_data: List[MachineStatus]) -> DataFrame:
    jsontxt = jsonable_encoder(prepared_data)
    dataframe = json_normalize(jsontxt)
    return dataframe


async def remove_outliers(data: DataFrame) -> DataFrame:
    print(len(data["totalAmount"]))

    # remove from the dataframe any row where the value
    # of the totalAmount column is greater or lower than 2 standard deviations
    # from the mean.
    upper_boundary = data["totalAmount"].mean() + 3 * data["totalAmount"].std()
    lower_boundary = data["totalAmount"].mean() - 3 * data["totalAmount"].std()
    data = data[
        (data["totalAmount"] < upper_boundary) & (data["totalAmount"] > lower_boundary)
    ]

    # remove from the dataframe any row where the value
    # of the totalAmount column is 0.
    data = data[data["totalAmount"] > 0]
    print(len(data["totalAmount"]))

    return data


async def convert_categorical_data(
    data: DataFrame, drop_first: bool = True
) -> DataFrame:
    converted = get_dummies(data=data, drop_first=drop_first)
    return converted


async def ordinal_encoder_categorical_data(
    data: DataFrame, drop_first: bool = True
) -> DataFrame:
    oe = OrdinalEncoder()
    oe.fit(data)
    data_enc = oe.transform(data)
    return data_enc
