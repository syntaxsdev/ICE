import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score



def generate_time_series_data(ticker, n, ticker_interval, min_price, max_price, min_volume, max_volume, num_moving_averages, moving_average_periods):
    # Calculate the number of trading days in the interval
    trading_days = pd.date_range(end=pd.Timestamp.today(), periods=n, freq=ticker_interval).strftime('%Y-%m-%d')
    
    # Initialize empty dataframe for the time series data
    time_series_data = pd.DataFrame(index=range(len(trading_days)), columns=['date', 'ticker', 'open', 'high', 'low', 'close', 'volume'])
    
    # Generate random price data that increases and decreases
    price_data = np.cumsum(np.random.normal(size=n)) + np.random.randint(low=min_price, high=max_price)
    price_data = np.maximum(price_data, np.zeros_like(price_data))  # prevent negative prices
    
    # Generate OHLCV data based on the price data
    ohlcv_data = []
    for i, price in enumerate(price_data):
        open_price = price - np.random.randint(low=1, high=10)
        close_price = price + np.random.randint(low=1, high=10)
        high_price = max(price, open_price, close_price) + np.random.randint(low=1, high=10)
        low_price = min(price, open_price, close_price) - np.random.randint(low=1, high=10)
        volume = np.random.randint(low=min_volume, high=max_volume)
        ohlcv_data.append((open_price, high_price, low_price, close_price, volume))
    ohlcv_data = np.array(ohlcv_data)
    
    # Generate moving average data that aligns with the price data
    moving_average_data = np.zeros((n, num_moving_averages))
    for i in range(num_moving_averages):
        period = moving_average_periods[i]
        moving_average_data[:,i] = np.convolve(price_data, np.ones((period,))/period, mode='same')
        
    # Set buy_signal to True if smallest moving average is greater than any of the other moving averages
    buy_signal = moving_average_data[:,0] > np.max(moving_average_data[:,1:], axis=1)
    
    # Store the generated data in the time series data dataframe
    time_series_data['date'] = trading_days
    time_series_data['ticker'] = ticker
    time_series_data[['open', 'high', 'low', 'close', 'volume']] = ohlcv_data
    for i in range(num_moving_averages):
        time_series_data[f'ma_{moving_average_periods[i]}'] = moving_average_data[:,i]
    time_series_data['buy_signal'] = buy_signal
    
    return time_series_data


data = generate_time_series_data('AAPL', 1000, '30min', 100, 200, 100000, 5000000, 3, [10, 50, 200])

from keras.models import Sequential
from keras.layers import Conv1D, MaxPooling1D, Flatten, Dense, Dropout

# Generate time series data
data = generate_time_series_data('AAPL', 1000, '1d', 100, 200, 100000, 5000000, 3, [20, 50, 100])

# Prepare the data for the CNN model
X = data.drop(['date', 'ticker', 'buy_signal'], axis=1).values.reshape((-1, X.shape[1], 1))
y = data['buy_signal'].values

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Instantiate and compile the CNN model
model = Sequential()
model.add(Conv1D(filters=32, kernel_size=3, activation='relu', input_shape=(X.shape[1], 1)))
model.add(MaxPooling1D(pool_size=2))
model.add(Conv1D(filters=64, kernel_size=3, activation='relu'))
model.add(MaxPooling1D(pool_size=2))
model.add(Flatten())
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the CNN model
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

# Predict the buy signal for the test data and calculate the accuracy
y_pred = model.predict(X_test)
y_pred = (y_pred > 0.5).astype(int)
accuracy = accuracy_score(y_test, y_pred)

print(f'Accuracy of CNN: {accuracy}')
