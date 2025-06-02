import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense


def predict_future(csv_path, target_year):
    df = pd.read_csv(csv_path, parse_dates=['date'])

    # Ensure 'ozone' column exists
    ozone_col = None
    for col in df.columns:
        if 'ozone' in col.lower():
            ozone_col = col
            break
    if ozone_col is None:
        raise ValueError("Missing 'ozone' column in dataset.")

    # Sort by date and set index
    df = df.sort_values('date')
    df.set_index('date', inplace=True)

    # Extract ozone data
    ozone_data = df[[ozone_col]].copy()

    # Normalize
    scaler = MinMaxScaler()
    ozone_scaled = scaler.fit_transform(ozone_data)

    # Prepare sequences for LSTM
    sequence_length = 12
    X, y = [], []
    for i in range(len(ozone_scaled) - sequence_length):
        X.append(ozone_scaled[i:i + sequence_length])
        y.append(ozone_scaled[i + sequence_length])

    X, y = np.array(X), np.array(y)

    # Build LSTM model
    model = Sequential()
    model.add(LSTM(64, activation='relu', input_shape=(sequence_length, 1)))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')

    # Train model
    model.fit(X, y, epochs=20, batch_size=8, verbose=0)

    # Predict next 48 months
    last_sequence = ozone_scaled[-sequence_length:]
    predictions = []
    for _ in range(48):
        pred = model.predict(last_sequence.reshape(1, sequence_length, 1), verbose=0)
        predictions.append(pred[0][0])
        last_sequence = np.append(last_sequence[1:], pred, axis=0)

    # Inverse scale predictions
    predicted_values = scaler.inverse_transform(np.array(predictions).reshape(-1, 1)).flatten()

    # Create date index
    start_date = df.index[-1] + pd.DateOffset(months=1)
    future_dates = pd.date_range(start=start_date, periods=48, freq='MS')
    prediction_df = pd.DataFrame({"date": future_dates, "predicted_ozone": predicted_values})
    prediction_df['year'] = prediction_df['date'].dt.year

    # Return predictions for the selected year
    return prediction_df[prediction_df['year'] == target_year]['predicted_ozone']
