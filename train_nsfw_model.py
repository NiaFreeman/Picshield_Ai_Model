"""
Train NSFW Detection Model
Uses the downloaded dataset to train a binary NSFW classifier
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
import os

print('TensorFlow version:', tf.__version__)

# Paths
downloaded_data = r'webapp\public\nsfw_data_scraper\data\train'
output_base = r'nsfw_dataset'

# Create merged dataset structure
print('\n' + '='*60)
print('Creating merged dataset...')
print('='*60)

os.makedirs(f'{output_base}/training/nsfw', exist_ok=True)
os.makedirs(f'{output_base}/training/safe', exist_ok=True)
os.makedirs(f'{output_base}/validation/nsfw', exist_ok=True)
os.makedirs(f'{output_base}/validation/safe', exist_ok=True)

# Data generators
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True,
    zoom_range=0.2,
    validation_split=0.2
)

train_generator = train_datagen.flow_from_directory(
    output_base,
    target_size=(150, 150),
    batch_size=32,
    class_mode='binary',
    subset='training'
)

validation_generator = train_datagen.flow_from_directory(
    output_base,
    target_size=(150, 150),
    batch_size=32,
    class_mode='binary',
    subset='validation'
)

print(f'\nTraining samples: {train_generator.samples}')
print(f'Validation samples: {validation_generator.samples}')

# Build model
print('\n' + '='*60)
print('Building model...')
print('='*60)

model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)),
    MaxPooling2D(2, 2),
    
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),
    
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),
    
    Flatten(),
    Dropout(0.5),
    Dense(512, activation='relu'),
    Dense(1, activation='sigmoid')
])

model.compile(
    loss='binary_crossentropy',
    optimizer='adam',
    metrics=['accuracy']
)

model.summary()

# Train
print('\n' + '='*60)
print('Training model...')
print('='*60)

history = model.fit(
    train_generator,
    steps_per_epoch=len(train_generator),
    epochs=20,
    validation_data=validation_generator,
    validation_steps=len(validation_generator)
)

# Save
print('\n' + '='*60)
print('Saving model...')
print('='*60)

model.save('models/nsfw_model.h5')
print('✓ Model saved as models/nsfw_model.h5')

# Convert to TFJS
print('\n' + '='*60)
print('Converting to TensorFlow.js...')
print('='*60)

os.system('tensorflowjs_converter --input_format=keras models/nsfw_model.h5 webapp/public/models/nsfw_model')
print('✓ Model converted for web use!')

print('\n' + '='*60)
print('TRAINING COMPLETE!')
print('='*60)
