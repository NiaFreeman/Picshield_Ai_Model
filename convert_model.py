import tensorflow as tf
from tensorflow import keras
import json
import os

print("Loading model...")
model = keras.models.load_model('models/nsfw_model.h5')

print("Converting to TensorFlow.js format...")
output_dir = 'webapp/public/models/nsfw_model'
os.makedirs(output_dir, exist_ok=True)

# Save as SavedModel first
print("Saving as SavedModel...")
model.export(output_dir + '_temp')

# Convert SavedModel to TF.js
print("Converting SavedModel to TF.js...")
os.system(f'tensorflowjs_converter --input_format=tf_saved_model {output_dir}_temp {output_dir}')

print("✓ Conversion complete!")
print(f"Model saved to: {output_dir}")
