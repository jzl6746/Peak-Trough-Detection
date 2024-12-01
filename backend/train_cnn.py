import numpy as np
import pandas as pd
from tensorflow.keras.callbacks import EarlyStopping
from cnn_model import CNNModel  # Assuming the CNNModel class is in cnn_model.py
from stock_data import fetch_stock_data_with_date_range  # Fetch historical stock data

def generate_training_data(data, window_size=50):
    """
    Preprocess stock data into sliding windows and labels.
    """
    prices = data['Close'].values
    windows, labels = [], []
    
    for i in range(len(prices) - window_size):
        window = prices[i:i + window_size]
        
        # Normalize the window
        window = (window - np.mean(window)) / np.std(window)

        # Default to "Neither" (class 0)
        label = 0 
        
        # Heuristic for labeling windows as peaks or troughs based on the data within the window
        is_peak = False
        is_trough = False
        
        # Check for peak: window should have a local maximum at the center (heuristic)
        if np.argmax(window) == window_size // 2:  # Check if the center of the window is the peak
            is_peak = True
        
        # Check for trough: window should have a local minimum at the center (heuristic)
        elif np.argmin(window) == window_size // 2:  # Check if the center of the window is the trough
            is_trough = True
        
        # Assign label based on the heuristics
        if is_peak:
            label = 1  # Peak
        elif is_trough:
            label = 2  # Trough
        
        windows.append(window)
        labels.append(label)
        
    # Print label distribution for debugging
    print(f"Label Distribution: {dict(zip(*np.unique(labels, return_counts=True)))}")
    
    return np.array(windows).reshape(-1, window_size, 1), np.array(labels)

# Load data and preprocess
ticker = "AAPL"
start_date = "2015-01-01"
end_date = "2020-12-31"
df = fetch_stock_data_with_date_range(ticker, start_date, end_date)

if df is not None:
    print(df.head())
else:
    print("Failed to fetch data.")

# Convert the start_date and end_date to datetime
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Ensure the DataFrame index is datetime for comparison
df.index = pd.to_datetime(df.index)

# Define parameters
window_size = 50

# Preprocess and generate training data
X, y = generate_training_data(df, window_size)
print("Input Shape:", X.shape)  # Should be (num_samples, 50, 1)
print("Label Shape:", y.shape)  # Should be (num_samples,)

# Check class distribution
unique, counts = np.unique(y, return_counts=True)
print("Class Distribution:", dict(zip(unique, counts)))

# Balance classes using class weights
from sklearn.utils.class_weight import compute_class_weight
class_weights = compute_class_weight('balanced', classes=np.unique(y), y=y)
class_weights_dict = dict(enumerate(class_weights))

# Create and train the CNN model
model = CNNModel.create_model(input_shape=(window_size, 1))
early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)


# Train the model
model.fit(
    X, y,
    validation_split=0.2,
    epochs=20,
    batch_size=32,
    callbacks=[early_stopping],
    class_weight=class_weights_dict  # Apply class weights
)

# Save the trained model
model.save("cnn_model.h5")
print("Model saved at cnn_model.h5")
