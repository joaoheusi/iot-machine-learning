import time
from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from src.modules.predictions.models.documents import MachineStatus
from src.modules.predictions.services.shared.fetch_data import fetch_data
from src.modules.predictions.services.shared.prepare_data import prepare_data
from src.shared.providers.pandas.utils import (
    json_to_dataframe,
    ordinal_encoder_categorical_data,
    remove_outliers,
)
from src.shared.providers.scikit_learn.neural_network import (
    generate_model,
    test_ann_model,
    train_ann_model,
)
from src.shared.providers.scikit_learn.utils import scale_datasets, split_dataset


async def transform_data_ann(prepared_flights: List[MachineStatus]):
    dataframe = await json_to_dataframe(prepared_flights)

    X = dataframe
    X = X.drop(
        ["failure"],
        axis=1,
    )
    X = await ordinal_encoder_categorical_data(data=X, drop_first=True)
    Y = dataframe["failure"]

    return X, Y


async def train_model_service(skip: int, limit: Optional[int]):
    machine_statuses = await fetch_data(skip, limit)
    prepared_machine_statuses = await prepare_data(machine_statuses)
    encoded_prepared_machine_statuses = jsonable_encoder(prepared_machine_statuses)

    X, Y = await transform_data_ann(encoded_prepared_machine_statuses)
    X_train, X_validate, y_train, y_validate = await split_dataset(X, Y, test_size=0.1)
    X_train, X_test, y_train, y_test = await split_dataset(
        X_train, y_train, test_size=0.1
    )
    X_train, X_test, X_validate = await scale_datasets(
        x_train=X_train, x_test=X_test, x_validate=X_validate
    )
    model = await generate_model(number_of_layers=7, number_of_nodes=27)
    trained_model = await train_ann_model(
        model,
        x_train=X_train,
        y_train=y_train,
        x_validate=X_validate,
        y_validate=y_validate,
        epochs=50,
    )
    score_loss, score_acc = await test_ann_model(
        model=trained_model,
        x_test=X_test,
        y_test=y_test,
    )

    response = {
        "score_loss": float(score_loss),
        "score_acc": float(score_acc),
    }
    model.save("ai_model/model")
    return response
