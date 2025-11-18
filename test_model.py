import tensorflow as tf
from tensorflow import keras
import numpy as np
from PIL import Image
import os

# Load model
print("Loading model...")
model = keras.models.load_model('models/nsfw_model.h5')

# Test with some images from the training dataset
test_dirs = {
    'NSFW': 'nsfw_dataset/training/nsfw',
    'Safe': 'nsfw_dataset/training/safe'
}

print("\n📊 Testing model predictions:")
print("=" * 60)

for label, dir_path in test_dirs.items():
    if not os.path.exists(dir_path):
        continue
    
    images = [f for f in os.listdir(dir_path) if f.endswith(('.jpg', '.jpeg', '.png'))][:5]
    
    print(f"\n{label} Images:")
    for img_file in images:
        img_path = os.path.join(dir_path, img_file)
        try:
            # Load and preprocess
            img = Image.open(img_path).convert('RGB')
            img = img.resize((150, 150))
            img_array = np.array(img) / 255.0
            img_tensor = np.expand_dims(img_array, axis=0)
            
            # Predict
            prediction = model.predict(img_tensor, verbose=0)[0][0]
            
            print(f"  {img_file[:30]:30s} -> {prediction:.4f} ({'NSFW' if prediction > 0.5 else 'Safe'})")
        except Exception as e:
            print(f"  {img_file[:30]:30s} -> Error: {e}")

print("\n" + "=" * 60)
print("\n💡 Interpretation:")
print("   - Values > 0.5 = NSFW")
print("   - Values < 0.5 = Safe")
print("\nIf NSFW images show low scores, the model may be inverted!")
