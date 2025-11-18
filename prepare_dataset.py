"""
Prepare NSFW Dataset - Merge downloaded images into training structure
"""

import os
import shutil
import glob
import numpy as np
from pathlib import Path

# Paths
downloaded_data = r'webapp\public\nsfw_data_scraper\data\train'
output_base = r'nsfw_dataset'

print('='*60)
print('MERGING NSFW DATASET')
print('='*60)

# Create directory structure
dirs = [
    f'{output_base}/training/nsfw',
    f'{output_base}/training/safe',
]

for d in dirs:
    Path(d).mkdir(parents=True, exist_ok=True)

print('✓ Directories created')

# Collect NSFW images (porn + hentai + sexy)
print('\nCollecting NSFW images...')
nsfw_images = []

for category in ['porn', 'hentai', 'sexy']:
    path = os.path.join(downloaded_data, category)
    if os.path.exists(path):
        imgs = glob.glob(os.path.join(path, '*.*'))
        nsfw_images.extend(imgs)
        print(f'  {category}: {len(imgs)} images')

print(f'Total NSFW: {len(nsfw_images)} images')

# Collect Safe images (neutral + drawings)
print('\nCollecting Safe images...')
safe_images = []

for category in ['neutral', 'drawings']:
    path = os.path.join(downloaded_data, category)
    if os.path.exists(path):
        imgs = glob.glob(os.path.join(path, '*.*'))
        safe_images.extend(imgs)
        print(f'  {category}: {len(imgs)} images')

print(f'Total Safe: {len(safe_images)} images')

# Copy NSFW images
print(f'\nCopying {len(nsfw_images)} NSFW images...')
for i, img in enumerate(nsfw_images):
    if i % 500 == 0:
        print(f'  Progress: {i}/{len(nsfw_images)}')
    try:
        shutil.copy(img, f'{output_base}/training/nsfw/')
    except Exception:
        pass

# Copy Safe images
print(f'\nCopying {len(safe_images)} Safe images...')
for i, img in enumerate(safe_images):
    if i % 500 == 0:
        print(f'  Progress: {i}/{len(safe_images)}')
    try:
        shutil.copy(img, f'{output_base}/training/safe/')
    except Exception:
        pass

print('\n' + '='*60)
print('DATASET READY!')
print('='*60)
print(f'Location: {output_base}/training/')
print(f'  nsfw/: {len(os.listdir(f"{output_base}/training/nsfw"))} images')
print(f'  safe/: {len(os.listdir(f"{output_base}/training/safe"))} images')
