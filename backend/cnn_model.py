from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam
import os

class CNNModel:
    @staticmethod
    def create_model(input_shape):
        """
        Create a 1D CNN model for stock prediction.
        """
        
        model = Sequential([
            # Convolutional layer
            Conv1D(filters=64, kernel_size=3, activation='relu', input_shape=input_shape),
            Dropout(0.2),
            
            # Add more layers as needed
            Conv1D(filters=32, kernel_size=3, activation='relu'),
            
            # Flatten before feeding into Dense layers
            Flatten(),
            
            # Dense layers
            Dense(128, activation='relu'),
            Dropout(0.3),
            Dense(3, activation='softmax')  # 3 classes: [0, 1, 2]
        ])
        
        
        """
        model = Sequential([
            Conv1D(64, kernel_size=3, activation='relu', input_shape=input_shape),
            MaxPooling1D(pool_size=2),
            Dropout(0.3),
            Flatten(),
            Dense(128, activation='relu'),
            Dropout(0.3),
            Dense(3, activation='softmax')
        ])
        """  
        
        model.compile(optimizer=Adam(learning_rate=0.0005), loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        return model

    @staticmethod
    def load_trained_model(model_path):
        """
        Loads a trained CNN model from the given path.
        """
        # If model_path is just a filename, build the absolute path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        absolute_model_path = os.path.join(current_dir, model_path)

        print(f"Loading model from: {absolute_model_path}")
        return load_model(absolute_model_path)

