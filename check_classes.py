import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Check what class indices were used during training
train_datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

train_generator = train_datagen.flow_from_directory(
    'nsfw_dataset/training',
    target_size=(150, 150),
    batch_size=32,
    class_mode='binary',
    subset='training'
)

print("Class indices used during training:")
print(train_generator.class_indices)
print("\nInterpretation:")
for class_name, class_index in train_generator.class_indices.items():
    print(f"  {class_name} -> {class_index}")

print("\n💡 In binary classification:")
print("   - Class 0 is the 'negative' class (first alphabetically)")
print("   - Class 1 is the 'positive' class (second alphabetically)")
print("\nSince folders are: nsfw, safe (alphabetical order)")
print("   - nsfw = 0")
print("   - safe = 1")
print("\n⚠️ THIS IS INVERTED! We want:")
print("   - nsfw = 1 (positive/sensitive)")
print("   - safe = 0 (negative/not sensitive)")
