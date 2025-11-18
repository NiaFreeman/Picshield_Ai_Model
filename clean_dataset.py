"""
Clean corrupted images from dataset
"""
import os
import glob
from PIL import Image

dataset_path = r'nsfw_dataset\training'
categories = ['nsfw', 'safe']

print('Scanning for corrupted images...')
removed = 0

for category in categories:
    path = os.path.join(dataset_path, category)
    images = glob.glob(os.path.join(path, '*.*'))
    
    print(f'\nChecking {category}: {len(images)} images')
    
    for img_path in images:
        try:
            with Image.open(img_path) as img:
                img.verify()  # Check if valid
        except Exception:
            print(f'  Removing corrupted: {os.path.basename(img_path)}')
            os.remove(img_path)
            removed += 1

print(f'\n✓ Removed {removed} corrupted images')
print('Dataset is clean!')
