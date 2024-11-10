import tensorflow as tf
import numpy as np
import argparse
import os

def train_model(epochs=10, batch_size=64, save_path=None):
    if save_path is None:
        save_path = os.path.join(os.path.dirname(__file__), 'saved_model.keras')

    # Load and preprocess MNIST dataset
    mnist = tf.keras.datasets.mnist
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    x_train, x_test = x_train / 255.0, x_test / 255.0

    # Create a simple sequential model
    model = tf.keras.models.Sequential([
        tf.keras.layers.Flatten(input_shape=(28, 28)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(10, activation='softmax')
    ])

    model.compile(optimizer='adam',
                 loss='sparse_categorical_crossentropy',
                 metrics=['accuracy'])

    # Train the model
    model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size)
    
    # Evaluate the model
    test_loss, test_accuracy = model.evaluate(x_test, y_test)
    print(f"Test accuracy: {test_accuracy}")
    
    # Save the model with .keras extension
    model.save(save_path)
    print(f"Model saved to {save_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Train MNIST digit recognition model')
    parser.add_argument('--epochs', type=int, default=5, help='Number of epochs')
    parser.add_argument('--batch-size', type=int, default=32, help='Batch size')
    parser.add_argument('--save-path', type=str, default=None, 
                      help='Path to save model (defaults to saved_model.keras in current directory)')
    
    args = parser.parse_args()
    train_model(args.epochs, args.batch_size, args.save_path)
