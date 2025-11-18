# Models Directory

This directory is for your AI model files.

## What to Put Here

- Model architecture definitions (e.g., `detection_model.py`)
- Preprocessing functions (e.g., `preprocessing.py`)
- Post-processing utilities
- Model configuration files

## Example Structure

```
models/
├── detection_model.py      # Main model architecture
├── preprocessing.py         # Image preprocessing
├── utils.py                # Helper functions
└── config.py               # Model configuration
```

## Usage Example

```python
# Example: Using your model
from models.detection_model import PicshieldModel

model = PicshieldModel()
model.load('path/to/weights.h5')
predictions = model.predict(image)
```

## Note

- Don't commit large model weight files (*.h5, *.pth) to Git
- Use .gitignore to exclude them
- Consider using Git LFS for large files
- Or store model weights externally (Google Drive, S3, etc.)
