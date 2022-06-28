from pandas import DataFrame
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler


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
