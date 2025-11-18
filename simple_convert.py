import tensorflow as tf
from tensorflow import keras
import os
import shutil
import json

# Load the model
print("Loading model...")
model = keras.models.load_model('models/nsfw_model.h5')

# Save as .keras format (newer format)
print("Saving as .keras format...")
model.save('models/nsfw_model.keras')

# Now use TensorFlow.js Python API to convert directly
print("Converting to TensorFlow.js...")
import tensorflowjs as tfjs

output_dir = 'webapp/public/models/nsfw_model'
os.makedirs(output_dir, exist_ok=True)

# Convert directly from Keras model
tfjs.converters.save_keras_model(model, output_dir)

print(f"\n✓ Model successfully converted to TensorFlow.js!")
print(f"✓ Output directory: {output_dir}")
print(f"✓ Check for model.json and weight files")

# List output files
if os.path.exists(output_dir):
    files = os.listdir(output_dir)
    print(f"\n📁 Files created: {files}")
