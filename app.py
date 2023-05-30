from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
import pandas_datareader.data as web
import datetime as dt
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/predict', methods=['GET'])
def predict():
    ticker = str(request.args.get('ticker'))
    end_date = str(request.args.get('end_date'))

    # Load the data
    df = yf.download(ticker, start='2012-01-01', end=end_date)

    # Create a new dataframe with only the 'Close' column
    data = df.filter(['Close'])

    # Convert the dataframe to a numpy array
    dataset = data.values

    # Get the number of rows to train the model on
    training_data_len = int(np.ceil(len(dataset) * 0.8))

    # Scale the data
    scaler = MinMaxScaler(feature_range=(0,1))
    scaled_data = scaler.fit_transform(dataset)

    # Create the scaled training data
    train_data = scaled_data[0:training_data_len, :]

    # Split the data into x_train and y_train datasets
    x_train = []
    y_train = []

    for i in range(60, len(train_data)):
        x_train.append(train_data[i-60:i, 0])
        y_train.append(train_data[i, 0])

    # Convert the x_train and y_train to numpy arrays
    x_train, y_train = np.array(x_train), np.array(y_train)

    # Reshape the data
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    # Build the LSTM model
    model = Sequential()

    model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
    model.add(Dropout(0.2))

    model.add(LSTM(units=50, return_sequences=True))
    model.add(Dropout(0.2))

    model.add(LSTM(units=50))
    model.add(Dropout(0.2))

    model.add(Dense(units=1))

    # Compile the model
    model.compile(optimizer='adam', loss='mean_squared_error')

    # Train the model
    model.fit(x_train, y_train, epochs=25, batch_size=32)

    # Create the testing data
    test_data = scaled_data[training_data_len - 60: , :]

    # Create the x_test and y_test datasets
    x_test = []
    y_test = dataset[training_data_len:, :]

    for i in range(60, len(test_data)):
        x_test.append(test_data[i-60:i, 0])

    # Convert the data to a numpy array
    x_test = np.array(x_test)

    # Reshape the data
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

    # Get the model's predicted price values
    predictions = model.predict(x_test)
    predictions = scaler.inverse_transform(predictions)

    # Process the predictions as needed
    # ...

    # Return the predictions as JSON response
    return jsonify({'predictions': predictions.tolist()})


if __name__ == '__main__':
    app.run(debug=True)
