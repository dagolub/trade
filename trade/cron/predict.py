import anyio
from trade.db.session import database as db
import pandas as pd  # type: ignore
from sklearn.preprocessing import MinMaxScaler  # type: ignore
from keras.models import Sequential  # type: ignore
from tensorflow.python.keras.layers.recurrent import LSTM  # type: ignore
from keras.layers.core import Dense  # type: ignore
import numpy as np
import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"


async def main():
    aggregation = [{"$group": {"_id": {"from_coin": "$from_coin", "to_coin": "$to_coin"}}}]
    pairs = []
    async for pair in db.exchange_mecx.aggregate(aggregation):
        if pair.get("_id").get("to_coin") == "USDT":
            pairs.append(
                {
                    "from_coin": pair.get("_id").get("from_coin"),
                    "to_coin": pair.get("_id").get("to_coin"),
                }
            )
            p = {
                "from_coin": pair.get("_id").get("from_coin"),
                "to_coin": pair.get("_id").get("to_coin"),
            }
            break

    data = []
    async for point in db.exchange_mecx.find({"from_coin": p.get("from_coin"), "to_coin": p.get("to_coin")}):
        data.append({"price": point.get("price"), "added": point.get("added")})

    data = pd.DataFrame.from_dict(data)

    scaler = MinMaxScaler(feature_range=(0, 1))
    # data.index = data.added
    data.drop("added", axis=1, inplace=True)
    final_data = data.values
    train_data = final_data[0:200, :]
    valid_data = final_data[200:, :]

    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(final_data)
    x_train_data, y_train_data = [], []
    for i in range(60, len(train_data)):
        x_train_data.append(scaled_data[i - 60 : i, 0])  # noqa
        y_train_data.append(scaled_data[i, 0])

    lstm_model = Sequential()
    lstm_model.add(LSTM(units=50, return_sequences=True, input_shape=(np.shape(x_train_data)[1], 1)))
    lstm_model.add(LSTM(units=50))
    lstm_model.add(Dense(1))
    model_data = data[len(data) - len(valid_data) - 60 :].values  # noqa
    model_data = model_data.reshape(-1, 1)
    model_data = scaler.transform(model_data)

    lstm_model.compile(loss="mean_squared_error", optimizer="adam")
    lstm_model.fit(x_train_data, y_train_data, epochs=1, batch_size=1, verbose=2)
    X_test = []
    for i in range(60, model_data.shape[0]):
        X_test.append(model_data[i - 60 : i, 0])  # noqa
    X_test = np.array(X_test)
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

    predicted_stock_price = lstm_model.predict(X_test)
    predicted_stock_price = scaler.inverse_transform(predicted_stock_price)
    pass


if __name__ == "__main__":
    anyio.run(main)
