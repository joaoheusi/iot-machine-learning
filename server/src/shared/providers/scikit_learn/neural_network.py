from typing import List

import pandas as pd
from keras.layers import Dense
from keras.models import Sequential
from sklearn.metrics import (
    mean_absolute_error,
    mean_absolute_percentage_error,
    r2_score,
)


async def generate_model(number_of_layers: int, number_of_nodes: int):
    model = Sequential()
    model.add(Dense(number_of_nodes, activation="relu"))
    model.add(Dense(number_of_nodes, activation="relu"))
    model.add(Dense(number_of_nodes, activation="relu"))
    model.add(Dense(number_of_nodes, activation="relu"))
    model.add(Dense(number_of_nodes, activation="relu"))
    model.add(Dense(number_of_nodes, activation="relu"))
    model.add(Dense(1))
    model.compile(optimizer="adam", loss="mae", metrics=["accuracy"])
    return model


async def train_ann_model(
    model: Sequential,
    x_train,
    y_train,
    x_validate,
    y_validate,
    batch_size: int = 128,
    epochs: int = 200,
):
    model.fit(
        x=x_train,
        y=y_train,
        validation_data=(x_validate, y_validate),
        batch_size=batch_size,
        epochs=epochs,
    )

    return model


async def test_ann_model(model: Sequential, x_test, y_test):
    predictions = model.predict(x_test)
    score = mean_absolute_error(y_test, predictions)
    score_percentage = mean_absolute_percentage_error(y_test, predictions)
    print(f"ScorePercentage: {score_percentage}")

    r2_score_value = r2_score(y_test, predictions)
    return score, r2_score_value, predictions
