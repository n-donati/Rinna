import tensorflow as tf
import numpy as np
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'saved_model.keras')

def create_model():
    # Load the pre-trained model
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"No trained model found at {MODEL_PATH}. Please run training first.")
    return tf.keras.models.load_model(MODEL_PATH)

def predict_digit(model, image_array):
    # Ensure image is 28x28 and normalized
    image_array = image_array.reshape(1, 28, 28)
    image_array = image_array / 255.0
    
    # Get prediction
    predictions = model.predict(image_array)
    return np.argmax(predictions[0])
