import tensorflow as tf
from tensorflow import keras
import numpy as np
from PIL import Image
import os

# Load model
print("Loading model...")
model = keras.models.load_model('models/nsfw_model.h5')

# Get model summary
print("\n" + "="*60)
print("MODEL ARCHITECTURE")
print("="*60)
model.summary()

# Test predictions on a few images
print("\n" + "="*60)
print("RAW MODEL OUTPUT (before inversion)")
print("="*60)
print("Remember: Model was trained with nsfw=0, safe=1")
print("So we expect: NSFW images → ~0.0, Safe images → ~1.0")
print("="*60 + "\n")

test_cases = [
    ('nsfw_dataset/training/nsfw', 'NSFW', 5),
    ('nsfw_dataset/training/safe', 'Safe', 5)
]

for dir_path, label, count in test_cases:
    if not os.path.exists(dir_path):
        print(f"❌ Directory not found: {dir_path}")
        continue
    
    images = [f for f in os.listdir(dir_path) if f.endswith(('.jpg', '.jpeg', '.png'))][:count]
    
    print(f"\n{label} Images:")
    scores = []
    for img_file in images:
        img_path = os.path.join(dir_path, img_file)
        try:
            img = Image.open(img_path).convert('RGB')
            img = img.resize((150, 150))
            img_array = np.array(img) / 255.0
            img_tensor = np.expand_dims(img_array, axis=0)
            
            raw_prediction = model.predict(img_tensor, verbose=0)[0][0]
            inverted_prediction = 1.0 - raw_prediction
            scores.append(inverted_prediction)
            
            print(f"  {img_file[:30]:30s} Raw: {raw_prediction:.4f} → Inverted: {inverted_prediction:.4f}")
        except Exception as e:
            print(f"  {img_file[:30]:30s} ERROR: {e}")
    
    if scores:
        print(f"  Average inverted score: {np.mean(scores):.4f} (std: {np.std(scores):.4f})")

print("\n" + "="*60)
print("INTERPRETATION")
print("="*60)
print("After inversion (what JavaScript sees):")
print("  - NSFW images should have HIGH scores (>0.75)")
print("  - Safe images should have LOW scores (<0.25)")
print("\nIf ALL scores are similar, the model didn't learn!")
print("="*60)
