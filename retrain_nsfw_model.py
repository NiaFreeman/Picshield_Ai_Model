"""
RETRAIN NSFW Model with Proper Settings
Fixes the degenerate solution problem
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
import os

print('TensorFlow version:', tf.__version__)

# Paths
dataset_path = 'nsfw_dataset/training'

# Data generators with proper augmentation
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True,
    zoom_range=0.2,
    validation_split=0.2,
    fill_mode='nearest'
)

# IMPORTANT: Set shuffle=True to prevent degenerate solutions
train_generator = train_datagen.flow_from_directory(
    dataset_path,
    target_size=(150, 150),
    batch_size=32,
    class_mode='binary',
    subset='training',
    shuffle=True,  # Critical!
    seed=42
)

validation_generator = train_datagen.flow_from_directory(
    dataset_path,
    target_size=(150, 150),
    batch_size=32,
    class_mode='binary',
    subset='validation',
    shuffle=True,
    seed=42
)

print(f'\nClass indices: {train_generator.class_indices}')
print(f'Training samples: {train_generator.samples}')
print(f'Validation samples: {validation_generator.samples}')

# Build model with batch normalization
from tensorflow.keras.layers import BatchNormalization

model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)),
    BatchNormalization(),
    MaxPooling2D(2, 2),
    
    Conv2D(64, (3, 3), activation='relu'),
    BatchNormalization(),
    MaxPooling2D(2, 2),
    
    Conv2D(128, (3, 3), activation='relu'),
    BatchNormalization(),
    MaxPooling2D(2, 2),
    
    Flatten(),
    Dropout(0.5),
    Dense(512, activation='relu'),
    Dropout(0.3),
    Dense(1, activation='sigmoid')
])

# Use a lower learning rate for better convergence
model.compile(
    loss='binary_crossentropy',
    optimizer=keras.optimizers.Adam(learning_rate=0.0001),
    metrics=['accuracy', keras.metrics.Precision(), keras.metrics.Recall()]
)

model.summary()

# Callbacks for better training
callbacks = [
    EarlyStopping(
        monitor='val_loss',
        patience=5,
        restore_best_weights=True
    ),
    ModelCheckpoint(
        'models/nsfw_model_best.h5',
        monitor='val_accuracy',
        save_best_only=True,
        verbose=1
    )
]

# Train
print('\n' + '='*60)
print('Training model...')
print('='*60)

history = model.fit(
    train_generator,
    epochs=30,
    validation_data=validation_generator,
    callbacks=callbacks,
    verbose=1
)

# Evaluate on validation set
print('\n' + '='*60)
print('Final Evaluation')
print('='*60)
val_loss, val_acc, val_prec, val_recall = model.evaluate(validation_generator)
print(f'Validation Accuracy: {val_acc:.4f}')
print(f'Validation Precision: {val_prec:.4f}')
print(f'Validation Recall: {val_recall:.4f}')

# Save
model.save('models/nsfw_model.h5')
print('\n✓ Model saved as models/nsfw_model.h5')
print('✓ Best model saved as models/nsfw_model_best.h5')

print('\n' + '='*60)
print('TRAINING COMPLETE!')
print('='*60)
print('Run proper_convert.py to convert to TensorFlow.js')
