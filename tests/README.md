# Tests Directory

This directory is for unit tests and integration tests.

## What to Put Here

- Unit tests for individual functions
- Integration tests for workflows
- Test fixtures and sample data
- Test configuration files

## Example Structure

```
tests/
├── test_model.py           # Model tests
├── test_preprocessing.py   # Preprocessing tests
├── test_inference.py       # Inference tests
├── fixtures/               # Test data
│   └── sample_image.jpg
└── conftest.py            # Pytest configuration
```

## Running Tests

```bash
# Install pytest
pip install pytest

# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_model.py

# Run with coverage
pip install pytest-cov
pytest --cov=models tests/
```

## Writing Tests

```python
# Example: test_preprocessing.py
import pytest
from models.preprocessing import preprocess_image

def test_preprocess_image():
    # Test that preprocessing works correctly
    image = load_test_image()
    processed = preprocess_image(image)
    assert processed.shape == (224, 224, 3)
    assert processed.max() <= 1.0
```

## Best Practices

- Test edge cases and error conditions
- Use descriptive test names
- Keep tests independent
- Mock external dependencies
- Aim for good code coverage
