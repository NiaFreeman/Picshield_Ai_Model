"""Resize and copy sample spicy images for demo and training.

This helper resizes up to N images from a source samples folder and
writes demo-sized images (512px) to the demo `examples` folder and
training-sized images (224px) under an inner `train/` folder.

Install dependency: `pip install pillow`
"""
import os
import argparse
from PIL import Image

def ensure_dir(p):
    if not os.path.exists(p):
        os.makedirs(p)

def resize_and_save(src_path, dest_path, size):
    with Image.open(src_path) as im:
        im = im.convert('RGB')
        im.thumbnail((size, size), Image.LANCZOS)
        im.save(dest_path, format='JPEG', quality=90)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--src', required=True, help='Source samples directory')
    parser.add_argument('--dest', required=True, help='Destination examples directory (relative to repo root)')
    parser.add_argument('--count', type=int, default=3, help='Number of sample images to copy')
    parser.add_argument('--demo_size', type=int, default=512, help='Pixel size for demo images')
    parser.add_argument('--train_size', type=int, default=224, help='Pixel size for training images')
    args = parser.parse_args()

    src = args.src
    dest = args.dest
    demo_size = args.demo_size
    train_size = args.train_size
    count = args.count

    ensure_dir(dest)
    train_dir = os.path.join(dest, 'train')
    ensure_dir(train_dir)

    # Find image files (jpg/jpeg/png)
    exts = ('.jpg', '.jpeg', '.png')
    files = [os.path.join(src, f) for f in os.listdir(src) if f.lower().endswith(exts)]
    files = sorted(files)

    if not files:
        print('No image files found in', src)
        return

    picked = files[:count]
    for i, path in enumerate(picked, start=1):
        demo_name = f'spicy_example_{i}.jpg'
        train_name = f'spicy_example_{i}_train.jpg'
        demo_dest = os.path.join(dest, demo_name)
        train_dest = os.path.join(train_dir, train_name)
        try:
            resize_and_save(path, demo_dest, demo_size)
            resize_and_save(path, train_dest, train_size)
            print('Saved', demo_dest, 'and', train_dest)
        except Exception as e:
            print('Error processing', path, e)

if __name__ == '__main__':
    main()
