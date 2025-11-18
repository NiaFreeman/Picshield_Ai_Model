# Sample Data Directory

This directory is for small sample datasets for testing and examples.

## Guidelines

- ✅ **Do**: Add small sample images for testing (< 100KB each)
- ✅ **Do**: Add example input/output pairs
- ✅ **Do**: Add data for unit tests
- ❌ **Don't**: Add large datasets (> 10MB)
- ❌ **Don't**: Add full training datasets

## Large Datasets

For large datasets:
1. Add them to `.gitignore`
2. Store them externally (Google Drive, AWS S3, etc.)
3. Add a `DATA.md` file with download instructions
4. Use tools like DVC for data versioning

## Example Structure

```
data/
├── sample/
│   ├── test_image_1.jpg
│   ├── test_image_2.jpg
│   └── expected_output.json
└── .gitkeep
```
