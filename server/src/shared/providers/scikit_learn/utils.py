import random

from pandas import DataFrame
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler


async def round_predict_score(float_score: float):
    # add a round value from 0 to 7 to the float_score
    # to make the score more round

    round_value_predi = random.randint(0, 100) / 23
    round_value = round(random.random() * 7)

    float_score = (float_score + round_value) * round_value_predi

    return float_score


async def scale_datasets(x_train, x_test, x_validate):
    scaler = MinMaxScaler()
    X_train = scaler.fit_transform(x_train)
    X_test = scaler.transform(x_test)
    X_validate = scaler.transform(x_validate)

    return X_train, X_test, X_validate


async def split_dataset(variables: DataFrame, outcomes: DataFrame, test_size: float):
    x_train, x_test, y_train, y_test = train_test_split(
        variables,
        outcomes,
        test_size=test_size,
        random_state=10,
    )
    return x_train, x_test, y_train, y_test
