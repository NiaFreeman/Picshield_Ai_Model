import tensorflow as tf
from tensorflow import keras
import numpy as np
import json
import os

# Load model
print("Loading model...")
model = keras.models.load_model('models/nsfw_model.h5')

# Create output directory
output_dir = 'webapp/public/models/nsfw_model'
os.makedirs(output_dir, exist_ok=True)

# Build proper model topology matching TF.js format
model_json = {
    "format": "layers-model",
    "generatedBy": "keras v2.4.0",
    "convertedBy": "Manual Conversion v1.0",
    "modelTopology": {
        "keras_version": "2.4.0",
        "backend": "tensorflow",
        "model_config": {
            "class_name": "Sequential",
            "config": {
                "name": "sequential",
                "layers": [
                    {
                        "class_name": "InputLayer",
                        "config": {
                            "batch_input_shape": [None, 150, 150, 3],
                            "dtype": "float32",
                            "sparse": False,
                            "ragged": False,
                            "name": "conv2d_input"
                        }
                    },
                    {
                        "class_name": "Conv2D",
                        "config": {
                            "name": "conv2d",
                            "trainable": True,
                            "batch_input_shape": [None, 150, 150, 3],
                            "dtype": "float32",
                            "filters": 32,
                            "kernel_size": [3, 3],
                            "strides": [1, 1],
                            "padding": "valid",
                            "data_format": "channels_last",
                            "dilation_rate": [1, 1],
                            "groups": 1,
                            "activation": "relu",
                            "use_bias": True,
                            "kernel_initializer": {"class_name": "GlorotUniform", "config": {"seed": None}},
                            "bias_initializer": {"class_name": "Zeros", "config": {}},
                            "kernel_regularizer": None,
                            "bias_regularizer": None,
                            "activity_regularizer": None,
                            "kernel_constraint": None,
                            "bias_constraint": None
                        }
                    },
                    {
                        "class_name": "BatchNormalization",
                        "config": {
                            "name": "batch_normalization",
                            "trainable": True,
                            "dtype": "float32",
                            "axis": [3],
                            "momentum": 0.99,
                            "epsilon": 0.001,
                            "center": True,
                            "scale": True,
                            "beta_initializer": {"class_name": "Zeros", "config": {}},
                            "gamma_initializer": {"class_name": "Ones", "config": {}},
                            "moving_mean_initializer": {"class_name": "Zeros", "config": {}},
                            "moving_variance_initializer": {"class_name": "Ones", "config": {}}
                        }
                    },
                    {
                        "class_name": "MaxPooling2D",
                        "config": {
                            "name": "max_pooling2d",
                            "trainable": True,
                            "dtype": "float32",
                            "pool_size": [2, 2],
                            "padding": "valid",
                            "strides": [2, 2],
                            "data_format": "channels_last"
                        }
                    },
                    {
                        "class_name": "Conv2D",
                        "config": {
                            "name": "conv2d_1",
                            "trainable": True,
                            "dtype": "float32",
                            "filters": 64,
                            "kernel_size": [3, 3],
                            "strides": [1, 1],
                            "padding": "valid",
                            "data_format": "channels_last",
                            "dilation_rate": [1, 1],
                            "groups": 1,
                            "activation": "relu",
                            "use_bias": True,
                            "kernel_initializer": {"class_name": "GlorotUniform", "config": {"seed": None}},
                            "bias_initializer": {"class_name": "Zeros", "config": {}},
                            "kernel_regularizer": None,
                            "bias_regularizer": None,
                            "activity_regularizer": None,
                            "kernel_constraint": None,
                            "bias_constraint": None
                        }
                    },
                    {
                        "class_name": "BatchNormalization",
                        "config": {
                            "name": "batch_normalization_1",
                            "trainable": True,
                            "dtype": "float32",
                            "axis": [3],
                            "momentum": 0.99,
                            "epsilon": 0.001,
                            "center": True,
                            "scale": True,
                            "beta_initializer": {"class_name": "Zeros", "config": {}},
                            "gamma_initializer": {"class_name": "Ones", "config": {}},
                            "moving_mean_initializer": {"class_name": "Zeros", "config": {}},
                            "moving_variance_initializer": {"class_name": "Ones", "config": {}}
                        }
                    },
                    {
                        "class_name": "MaxPooling2D",
                        "config": {
                            "name": "max_pooling2d_1",
                            "trainable": True,
                            "dtype": "float32",
                            "pool_size": [2, 2],
                            "padding": "valid",
                            "strides": [2, 2],
                            "data_format": "channels_last"
                        }
                    },
                    {
                        "class_name": "Conv2D",
                        "config": {
                            "name": "conv2d_2",
                            "trainable": True,
                            "dtype": "float32",
                            "filters": 128,
                            "kernel_size": [3, 3],
                            "strides": [1, 1],
                            "padding": "valid",
                            "data_format": "channels_last",
                            "dilation_rate": [1, 1],
                            "groups": 1,
                            "activation": "relu",
                            "use_bias": True,
                            "kernel_initializer": {"class_name": "GlorotUniform", "config": {"seed": None}},
                            "bias_initializer": {"class_name": "Zeros", "config": {}},
                            "kernel_regularizer": None,
                            "bias_regularizer": None,
                            "activity_regularizer": None,
                            "kernel_constraint": None,
                            "bias_constraint": None
                        }
                    },
                    {
                        "class_name": "BatchNormalization",
                        "config": {
                            "name": "batch_normalization_2",
                            "trainable": True,
                            "dtype": "float32",
                            "axis": [3],
                            "momentum": 0.99,
                            "epsilon": 0.001,
                            "center": True,
                            "scale": True,
                            "beta_initializer": {"class_name": "Zeros", "config": {}},
                            "gamma_initializer": {"class_name": "Ones", "config": {}},
                            "moving_mean_initializer": {"class_name": "Zeros", "config": {}},
                            "moving_variance_initializer": {"class_name": "Ones", "config": {}}
                        }
                    },
                    {
                        "class_name": "MaxPooling2D",
                        "config": {
                            "name": "max_pooling2d_2",
                            "trainable": True,
                            "dtype": "float32",
                            "pool_size": [2, 2],
                            "padding": "valid",
                            "strides": [2, 2],
                            "data_format": "channels_last"
                        }
                    },
                    {
                        "class_name": "Flatten",
                        "config": {
                            "name": "flatten",
                            "trainable": True,
                            "dtype": "float32",
                            "data_format": "channels_last"
                        }
                    },
                    {
                        "class_name": "Dropout",
                        "config": {
                            "name": "dropout",
                            "trainable": True,
                            "dtype": "float32",
                            "rate": 0.5,
                            "noise_shape": None,
                            "seed": None
                        }
                    },
                    {
                        "class_name": "Dense",
                        "config": {
                            "name": "dense",
                            "trainable": True,
                            "dtype": "float32",
                            "units": 512,
                            "activation": "relu",
                            "use_bias": True,
                            "kernel_initializer": {"class_name": "GlorotUniform", "config": {"seed": None}},
                            "bias_initializer": {"class_name": "Zeros", "config": {}},
                            "kernel_regularizer": None,
                            "bias_regularizer": None,
                            "activity_regularizer": None,
                            "kernel_constraint": None,
                            "bias_constraint": None
                        }
                    },
                    {
                        "class_name": "Dropout",
                        "config": {
                            "name": "dropout_1",
                            "trainable": True,
                            "dtype": "float32",
                            "rate": 0.3,
                            "noise_shape": None,
                            "seed": None
                        }
                    },
                    {
                        "class_name": "Dense",
                        "config": {
                            "name": "dense_1",
                            "trainable": True,
                            "dtype": "float32",
                            "units": 1,
                            "activation": "sigmoid",
                            "use_bias": True,
                            "kernel_initializer": {"class_name": "GlorotUniform", "config": {"seed": None}},
                            "bias_initializer": {"class_name": "Zeros", "config": {}},
                            "kernel_regularizer": None,
                            "bias_regularizer": None,
                            "activity_regularizer": None,
                            "kernel_constraint": None,
                            "bias_constraint": None
                        }
                    }
                ]
            }
        },
        "training_config": {
            "loss": "binary_crossentropy",
            "metrics": [[{"class_name": "MeanMetricWrapper", "config": {"name": "accuracy", "dtype": "float32", "fn": "binary_accuracy"}}]],
            "weighted_metrics": None,
            "loss_weights": None,
            "optimizer_config": {
                "class_name": "Adam",
                "config": {
                    "name": "Adam",
                    "learning_rate": 0.001,
                    "decay": 0.0,
                    "beta_1": 0.9,
                    "beta_2": 0.999,
                    "epsilon": 1e-07,
                    "amsgrad": False
                }
            }
        }
    },
    "weightsManifest": []
}

# Extract weights with proper naming
print("Extracting weights...")
weight_specs = []
all_weights = []

# Get weights from each layer - NEW MODEL HAS BATCHNORM LAYERS
# Layer indices: Conv2D(0), BatchNorm(1), MaxPool(2), Conv2D(3), BatchNorm(4), MaxPool(5), Conv2D(6), BatchNorm(7), MaxPool(8), Flatten(9), Dropout(10), Dense(11), Dropout(12), Dense(13)
layer_weights = {
    'conv2d': model.layers[0].get_weights(),
    'batch_normalization': model.layers[1].get_weights(),
    'conv2d_1': model.layers[3].get_weights(),
    'batch_normalization_1': model.layers[4].get_weights(),
    'conv2d_2': model.layers[6].get_weights(),
    'batch_normalization_2': model.layers[7].get_weights(),
    'dense': model.layers[11].get_weights(),
    'dense_1': model.layers[13].get_weights()
}

for layer_name, weights in layer_weights.items():
    if layer_name.startswith('batch_normalization'):
        # BatchNorm has 4 weights: gamma, beta, moving_mean, moving_variance
        if len(weights) == 4:
            gamma, beta, moving_mean, moving_variance = weights
            weight_specs.append({"name": f"{layer_name}/gamma", "shape": list(gamma.shape), "dtype": "float32"})
            all_weights.append(gamma.flatten())
            weight_specs.append({"name": f"{layer_name}/beta", "shape": list(beta.shape), "dtype": "float32"})
            all_weights.append(beta.flatten())
            weight_specs.append({"name": f"{layer_name}/moving_mean", "shape": list(moving_mean.shape), "dtype": "float32"})
            all_weights.append(moving_mean.flatten())
            weight_specs.append({"name": f"{layer_name}/moving_variance", "shape": list(moving_variance.shape), "dtype": "float32"})
            all_weights.append(moving_variance.flatten())
    elif len(weights) == 2:  # kernel and bias (Conv2D, Dense)
        kernel, bias = weights
        # Add kernel
        weight_specs.append({
            "name": f"{layer_name}/kernel",
            "shape": list(kernel.shape),
            "dtype": "float32"
        })
        all_weights.append(kernel.flatten())
        
        # Add bias
        weight_specs.append({
            "name": f"{layer_name}/bias",
            "shape": list(bias.shape),
            "dtype": "float32"
        })
        all_weights.append(bias.flatten())

# Concatenate all weights
weights_data = np.concatenate(all_weights)

# Save as binary
print("Saving weights...")
weights_file = os.path.join(output_dir, 'group1-shard1of1.bin')
with open(weights_file, 'wb') as f:
    f.write(weights_data.astype(np.float32).tobytes())

# Update manifest
model_json["weightsManifest"] = [{
    "paths": ["group1-shard1of1.bin"],
    "weights": weight_specs
}]

# Save model.json
model_file = os.path.join(output_dir, 'model.json')
with open(model_file, 'w') as f:
    json.dump(model_json, f, indent=2)

print(f"\n✅ Conversion complete!")
print(f"✅ Created: {model_file}")
print(f"✅ Created: {weights_file}")
print(f"✅ Total weight size: {len(weights_data) * 4 / (1024*1024):.2f} MB")
print(f"✅ Number of weight tensors: {len(weight_specs)}")
print(f"\n📊 Weight manifest:")
for spec in weight_specs:
    print(f"   {spec['name']}: {spec['shape']}")
