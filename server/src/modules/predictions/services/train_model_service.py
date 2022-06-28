import time
from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from src.modules.analysis.predictions.shared.fetch_data import fetch_data
from src.modules.analysis.predictions.shared.prepare_data import prepare_data
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


async def transform_data_ann(prepared_flights: List[FlightPreparedData]):
    # Function that takes in a FlightInfo-like object and turns it into
    # the correct type of object to run the multiple linear regression.

    dataframe = await json_to_dataframe(prepared_flights)
    dataframe = await remove_outliers(dataframe)

    dataframe = dataframe.drop(
        [
            "issueDate",
            "departureDate",
            "arrivalDate",
            "requestDate",
        ],
        axis=1,
    )
    X = dataframe
    X = X.drop(
        ["totalAmount"],
        axis=1,
    )
    X = await ordinal_encoder_categorical_data(data=X, drop_first=True)
    Y = dataframe["totalAmount"]

    return X, Y


async def neural_network_service(skip: int, limit: Optional[int]):
    flights = await fetch_data(skip, limit)
    start = time.time()
    prepared_flights = await prepare_data(flights)
    sample_flight_data = prepared_flights[0].dict()
    sample_flight_data.__delitem__("totalAmount")
    sample_flight_data.__delitem__("issueDate")
    sample_flight_data.__delitem__("departureDate")
    sample_flight_data.__delitem__("arrivalDate")
    sample_flight_data.__delitem__("requestDate")
    # delete all items in sample_flight_data where the value is None
    for key in list(sample_flight_data):
        if sample_flight_data.get(key) is None:
            sample_flight_data.__delitem__(key)
    print(sample_flight_data)
    encoded_prepared_flights = jsonable_encoder(prepared_flights)

    X, Y = await transform_data_ann(encoded_prepared_flights)
    X_train, X_validate, y_train, y_validate = await split_dataset(X, Y, test_size=0.1)
    X_train, X_test, y_train, y_test = await split_dataset(
        X_train, y_train, test_size=0.1
    )
    X_train, X_test, X_validate = await scale_datasets(
        x_train=X_train, x_test=X_test, x_validate=X_validate
    )
    print(len(list(sample_flight_data.keys())))
    model = await generate_model(
        number_of_layers=7, number_of_nodes=len(list(sample_flight_data.keys()))
    )
    trained_model, summed_weights = await train_ann_model(
        model,
        x_train=X_train,
        y_train=y_train,
        x_validate=X_validate,
        y_validate=y_validate,
        epochs=50,
    )
    score, r2_score_value, predictions = await test_ann_model(
        model=trained_model,
        x_test=X_test,
        y_test=y_test,
    )
    end = time.time()
    print(f"Time taken Neural Network: {end - start}")
    sample_keys = list(sample_flight_data.keys())

    # create a dict where the keys the items in sample_keys and the values are the
    # summed weights

    summed_weights_dict = {
        key: value for key, value in zip(sample_keys, summed_weights)
    }
    # create a dict where summed_weights_dict is ordered by the value
    ordered_coeffs = dict(
        sorted(summed_weights_dict.items(), key=lambda kv: kv[1], reverse=True)
    )
    response = {
        "meanAbsoluteError": score,
        "r2_score": r2_score_value,
        "coefficients": summed_weights_dict,
        "orderdCoefficients": ordered_coeffs,
    }

    return response
