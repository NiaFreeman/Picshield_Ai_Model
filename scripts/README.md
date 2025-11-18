# Scripts Directory

This directory is for executable scripts and utilities.

## What to Put Here

- Training scripts (e.g., `train.py`)
- Evaluation scripts (e.g., `evaluate.py`)
- Data processing scripts
- Utility scripts

## Example Structure

```
scripts/
├── train.py              # Training script
├── evaluate.py           # Model evaluation
├── preprocess_data.py    # Data preprocessing
└── inference.py          # Run inference on new images
```

## Usage Example

```bash
# Train the model
python scripts/train.py --epochs 50 --batch-size 32

# Evaluate the model
python scripts/evaluate.py --model-path models/checkpoint.h5

# Run inference
python scripts/inference.py --image test.jpg
```

## Tips

- Use command-line arguments for flexibility (argparse)
- Add help messages (`--help` flag)
- Include logging for debugging
- Make scripts modular and reusable
