# Contributing to Picshield AI Model

Thank you for contributing to Picshield AI Model! This guide will help you get started.

## Getting Started

1. **Fork and Clone**
   ```bash
   git clone https://github.com/NiaFreeman/Picshield_Ai_Model.git
   cd Picshield_Ai_Model
   ```

2. **Set Up Your Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt  # When added
   ```

## How to Upload Your Work

### Step-by-Step Guide

1. **Check Current Status**
   ```bash
   git status
   ```

2. **Add Your Files**
   - For a new folder: `git add folder-name/`
   - For specific files: `git add file1.py file2.py`
   - For all changes: `git add .`

3. **Commit Your Changes**
   ```bash
   git commit -m "Brief description of changes"
   ```

4. **Push to GitHub**
   ```bash
   git push origin main
   ```

### Showing Your Changes

**Before Committing:**
- `git diff` - See what changed in your files
- `git status` - See which files are modified

**After Committing:**
- `git log` - See your commit history
- Visit GitHub to see changes online

**On GitHub:**
- Go to: https://github.com/NiaFreeman/Picshield_Ai_Model/commits
- Click on any commit to see the detailed changes

## Project Structure

We recommend organizing the project as follows:

```
Picshield_Ai_Model/
│
├── models/              # AI model files
│   ├── detection_model.py
│   └── preprocessing.py
│
├── data/                # Datasets (consider using .gitignore for large files)
│   ├── training/
│   └── validation/
│
├── scripts/             # Utility scripts
│   ├── train.py
│   └── evaluate.py
│
├── notebooks/           # Jupyter notebooks
│   └── exploration.ipynb
│
├── tests/               # Unit tests
│   └── test_model.py
│
├── docs/                # Documentation
│   └── model_architecture.md
│
├── requirements.txt     # Python dependencies
├── .gitignore          # Files to ignore
├── README.md           # Main documentation
└── CONTRIBUTING.md     # This file
```

## Best Practices

### Commit Messages

Write clear, descriptive commit messages:

**Good Examples:**
- ✅ `Add CNN model for image classification`
- ✅ `Fix bug in preprocessing pipeline`
- ✅ `Update training script with new parameters`
- ✅ `Add unit tests for detection model`

**Bad Examples:**
- ❌ `Update`
- ❌ `Fix stuff`
- ❌ `Changes`

### What to Commit

**DO commit:**
- Source code (.py files)
- Documentation (.md files)
- Configuration files
- Small test datasets (< 1MB)
- Requirements files

**DON'T commit:**
- Large model files (use Git LFS or external storage)
- Large datasets (use .gitignore)
- Virtual environments (venv/, env/)
- IDE settings (.idea/, .vscode/)
- Temporary files (*.pyc, __pycache__/)
- Credentials or API keys (.env files)

### Code Quality

1. **Follow PEP 8** for Python code style
2. **Add docstrings** to functions and classes
3. **Write tests** for new features
4. **Update documentation** when changing functionality

## Workflow for New Features

1. **Create a branch** (optional, for larger changes)
   ```bash
   git checkout -b feature-name
   ```

2. **Make your changes**
   - Write code
   - Add tests
   - Update docs

3. **Test your changes**
   ```bash
   python -m pytest tests/  # If tests exist
   ```

4. **Commit and push**
   ```bash
   git add .
   git commit -m "Add [feature description]"
   git push origin feature-name
   ```

5. **Create a Pull Request** on GitHub

## Common Issues and Solutions

### Issue: "Nothing to commit"
**Solution:** Make sure you've actually changed files and added them with `git add`

### Issue: "Push rejected"
**Solution:** Pull first, resolve conflicts if any, then push
```bash
git pull origin main
git push origin main
```

### Issue: "Large files"
**Solution:** Add to .gitignore or use Git LFS
```bash
echo "large_file.h5" >> .gitignore
git rm --cached large_file.h5
```

### Issue: "Accidentally committed sensitive data"
**Solution:** Remove from Git history (advanced)
```bash
git rm --cached sensitive_file.txt
git commit -m "Remove sensitive file"
# Then ask for help removing from history
```

## Getting Help

- Check the [README.md](README.md) for basic Git workflow
- Check [GIT_WORKFLOW.md](GIT_WORKFLOW.md) for quick reference
- Open an issue on GitHub for questions
- Review Git documentation: https://git-scm.com/doc

## Code Review Process

1. Submit your changes via Pull Request
2. Wait for review and feedback
3. Address any comments or requested changes
4. Once approved, changes will be merged

## Style Guide

### Python Code
- Use 4 spaces for indentation
- Maximum line length: 88 characters (Black formatter)
- Use meaningful variable names
- Add type hints where appropriate

### Documentation
- Use Markdown for documentation files
- Include code examples where helpful
- Keep language clear and concise

## Testing

Before submitting changes:

1. Test your code locally
2. Run existing tests (if any)
3. Add tests for new features
4. Ensure no existing functionality breaks

## Questions?

If you're unsure about anything:
1. Check this guide and the README
2. Look at existing code for examples
3. Open an issue asking for clarification
4. Don't hesitate to ask for help!

---

Thank you for contributing to Picshield AI Model! 🎉
