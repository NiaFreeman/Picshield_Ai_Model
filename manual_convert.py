import tensorflow as tf
from tensorflow import keras
import numpy as np
import json
import os
import struct

# Load model
print("Loading model...")
model = keras.models.load_model('models/nsfw_model.h5')

# Create output directory
output_dir = 'webapp/public/models/nsfw_model'
os.makedirs(output_dir, exist_ok=True)

# Get model architecture as JSON
model_json = {
    "format": "layers-model",
    "generatedBy": "keras v" + tf.__version__,
    "convertedBy": "Manual Conversion",
    "modelTopology": {
        "class_name": "Sequential",
        "config": {
            "name": "sequential",
            "layers": []
        },
        "keras_version": "3.0.0",
        "backend": "tensorflow"
    },
    "weightsManifest": [{
        "paths": ["group1-shard1of1.bin"],
        "weights": []
    }]
}

# Build layers list
layers = [
    {
        "class_name": "Conv2D",
        "config": {
            "name": "conv2d",
            "filters": 32,
            "kernel_size": [3, 3],
            "strides": [1, 1],
            "padding": "valid",
            "activation": "relu",
            "use_bias": True,
            "dtype": "float32",
            "batch_input_shape": [None, 150, 150, 3]
        }
    },
    {
        "class_name": "MaxPooling2D",
        "config": {
            "name": "max_pooling2d",
            "pool_size": [2, 2],
            "strides": [2, 2],
            "padding": "valid"
        }
    },
    {
        "class_name": "Conv2D",
        "config": {
            "name": "conv2d_1",
            "filters": 64,
            "kernel_size": [3, 3],
            "strides": [1, 1],
            "padding": "valid",
            "activation": "relu",
            "use_bias": True
        }
    },
    {
        "class_name": "MaxPooling2D",
        "config": {
            "name": "max_pooling2d_1",
            "pool_size": [2, 2],
            "strides": [2, 2],
            "padding": "valid"
        }
    },
    {
        "class_name": "Conv2D",
        "config": {
            "name": "conv2d_2",
            "filters": 128,
            "kernel_size": [3, 3],
            "strides": [1, 1],
            "padding": "valid",
            "activation": "relu",
            "use_bias": True
        }
    },
    {
        "class_name": "MaxPooling2D",
        "config": {
            "name": "max_pooling2d_2",
            "pool_size": [2, 2],
            "strides": [2, 2],
            "padding": "valid"
        }
    },
    {
        "class_name": "Flatten",
        "config": {
            "name": "flatten"
        }
    },
    {
        "class_name": "Dropout",
        "config": {
            "name": "dropout",
            "rate": 0.5
        }
    },
    {
        "class_name": "Dense",
        "config": {
            "name": "dense",
            "units": 512,
            "activation": "relu",
            "use_bias": True
        }
    },
    {
        "class_name": "Dense",
        "config": {
            "name": "dense_1",
            "units": 1,
            "activation": "sigmoid",
            "use_bias": True
        }
    }
]

model_json["modelTopology"]["config"]["layers"] = layers

# Extract weights
print("Extracting weights...")
all_weights = []
weight_specs = []

for layer in model.layers:
    weights = layer.get_weights()
    if len(weights) > 0:
        for i, w in enumerate(weights):
            weight_name = f"{layer.name}/{'kernel' if i == 0 else 'bias'}:0"
            all_weights.append(w.flatten())
            weight_specs.append({
                "name": weight_name,
                "shape": list(w.shape),
                "dtype": "float32"
            })

# Concatenate all weights
print("Saving weights...")
weights_data = np.concatenate(all_weights)

# Save as binary
weights_file = os.path.join(output_dir, 'group1-shard1of1.bin')
with open(weights_file, 'wb') as f:
    f.write(weights_data.astype(np.float32).tobytes())

# Update manifest
model_json["weightsManifest"][0]["weights"] = weight_specs

# Save model.json
model_file = os.path.join(output_dir, 'model.json')
with open(model_file, 'w') as f:
    json.dump(model_json, f, indent=2)

print(f"\n✅ Conversion complete!")
print(f"✅ Created: {model_file}")
print(f"✅ Created: {weights_file}")
print(f"✅ Total weight size: {len(weights_data) * 4 / (1024*1024):.2f} MB")
print(f"✅ Number of weight tensors: {len(weight_specs)}")
