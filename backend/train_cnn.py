import numpy as np
import pandas as pd
from tensorflow.keras.callbacks import EarlyStopping
from cnn_model import CNNModel  # Assuming the CNNModel class is in cnn_model.py
from stock_data import fetch_stock_data_with_date_range  # Fetch historical stock data
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report

def generate_training_data(data, window_size=50):
    """
    Preprocess stock data into sliding windows and labels.
    """
    # Normalize all features except labels
    features = data[['Open', 'High', 'Low', 'Close', 'Volume', 'SMA_10']].values
    windows, labels = [], []
    
    for i in range(len(features) - window_size):
        window = features[i:i + window_size]
        
        # Normalize each feature separately across the window
        window_normalized = (window - np.mean(window, axis=0)) / np.std(window, axis=0)
        
        # Default to "Neither" (class 0)
        label = 0 
        
        # Combine price and volume data to refine labeling
        aggregated_prices = np.mean(window[:, :4], axis=1)  # Average of price-related features
        normalized_volume = (window[:, 4] - np.mean(window[:, 4])) / np.std(window[:, 4])  # Normalize volume
        
        # Weight aggregated prices and volume
        weighted_metric = 0.8 * aggregated_prices + 0.2 * normalized_volume
        
        is_peak = np.argmax(weighted_metric) == window_size // 2
        is_trough = np.argmin(weighted_metric) == window_size // 2

        
        if is_peak:
            label = 1  # Peak
        elif is_trough:
            label = 2  # Trough
        
        windows.append(window_normalized)
        labels.append(label)
        
    # Print label distribution for debugging
    print(f"Label Distribution: {dict(zip(*np.unique(labels, return_counts=True)))}")
    
    return np.array(windows), np.array(labels)

def augment_minority_class(X, y, target_class, num_samples):
    idx = np.where(y == target_class)[0]
    samples = X[idx]
    augmented_samples = []
    for i in range(num_samples):
        sample = samples[np.random.randint(len(samples))]
        noise = np.random.normal(0, 0.01, sample.shape)
        augmented_samples.append(sample + noise)
    return np.array(augmented_samples), np.full(num_samples, target_class)

# Load data and preprocess
ticker = "AAPL"
start_date = "2015-01-01"
end_date = "2020-12-31"
df = fetch_stock_data_with_date_range(ticker, start_date, end_date)
df['SMA_10'] = df['Close'].rolling(window=10).mean()
df['SMA_10'].fillna(method='bfill', inplace=True)  # Backfill with the next valid value

if df is not None:
    print(df.head())
else:
    print("Failed to fetch data.")

#normalization
df = (df - df.min()) / (df.max() - df.min())

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

# Step 1: Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
X_aug_peak, y_aug_peak = augment_minority_class(X_train, y_train, target_class=1, num_samples=100)
X_aug_trough, y_aug_trough = augment_minority_class(X_train, y_train, target_class=2, num_samples=100)
X_train = np.concatenate([X_train, X_aug_peak, X_aug_trough])
y_train = np.concatenate([y_train, y_aug_peak, y_aug_trough])

print("Training Shape:", X_train.shape)
print("Testing Shape:", X_test.shape)

from imblearn.over_sampling import SMOTE

smote = SMOTE(sampling_strategy='auto', random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_train.reshape(X_train.shape[0], -1), y_train)
X_resampled = X_resampled.reshape(-1, window_size, 6)



# Check class distribution
unique, counts = np.unique(y, return_counts=True)
print("Class Distribution:", dict(zip(unique, counts)))

# Balance classes using class weights
from sklearn.utils.class_weight import compute_class_weight
#class_weights = compute_class_weight('balanced', classes=np.unique(y), y=y)
#class_weights_dict = dict(enumerate(class_weights))
class_weights_dict = {0: 1.0, 1: 20.0, 2: 20.0}

# Create and train the CNN model
model = CNNModel.create_model(input_shape=(window_size, 6))
early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)


# Train the model
model.fit(
    X_resampled, y_resampled,
    validation_split=0.2,
    epochs=20,
    batch_size=32,
    callbacks=[early_stopping],
    class_weight=class_weights_dict  # Apply class weights
)

# Step 3: Evaluate the model on the test data
y_pred = model.predict(X_test)
y_pred_classes = np.argmax(y_pred, axis=1)  # Convert softmax output to class predictions

# Step 4: Generate the confusion matrix
conf_matrix = confusion_matrix(y_test, y_pred_classes)

# Optionally, print a classification report for more metrics
print(confusion_matrix(y_test, y_pred_classes))
print(classification_report(y_test, y_pred_classes, target_names=['Neither', 'Peak', 'Trough']))

# Save the trained model
model.save("cnn_model.h5")
print("Model saved at cnn_model.h5")
























