# Picshield AI Model

## How to Upload Your Folder / Show New Changes to Your Work

This guide explains how to add files, commit changes, and push them to GitHub.

### Prerequisites

- Git installed on your computer
- A GitHub account
- Repository cloned to your local machine

### Quick Start: Adding Files and Folders

#### 1. Clone the Repository (First Time Only)

```bash
git clone https://github.com/NiaFreeman/Picshield_Ai_Model.git
cd Picshield_Ai_Model
```

#### 2. Check Current Status

Before making changes, see what's in your repository:

```bash
git status
```

This shows:
- Which branch you're on
- Files that have been modified
- Files that are untracked (new files)

#### 3. Add Your Folder or Files

To add a specific folder:
```bash
git add your-folder-name/
```

To add specific files:
```bash
git add filename.py
git add another-file.txt
```

To add all new and modified files:
```bash
git add .
```

⚠️ **Warning**: Using `git add .` adds everything, including temporary files. It's better to be specific.

#### 4. View Your Changes

Before committing, review what will be included:

```bash
# See which files will be committed
git status

# See detailed changes in files
git diff

# See changes in files already staged
git diff --staged
```

#### 5. Commit Your Changes

Save your changes with a descriptive message:

```bash
git commit -m "Add your descriptive message here"
```

**Good commit message examples:**
- `git commit -m "Add initial AI model training script"`
- `git commit -m "Update image preprocessing functions"`
- `git commit -m "Fix bug in detection algorithm"`

#### 6. Push Changes to GitHub

Upload your commits to GitHub:

```bash
git push origin main
```

If you're on a different branch:
```bash
git push origin your-branch-name
```

### Complete Workflow Example

Here's a complete example of adding a new AI model folder:

```bash
# 1. Navigate to your repository
cd Picshield_Ai_Model

# 2. Create or add your folder
# (You can also copy files here using your file manager)
mkdir models
cp /path/to/your/model.py models/

# 3. Check what's new
git status

# 4. Add your new folder
git add models/

# 5. Commit with a message
git commit -m "Add image detection model"

# 6. Push to GitHub
git push origin main

# 7. Verify your changes on GitHub
# Visit: https://github.com/NiaFreeman/Picshield_Ai_Model
```

### Viewing Your Changes Online

After pushing, view your changes on GitHub:

1. Go to: https://github.com/NiaFreeman/Picshield_Ai_Model
2. You'll see your latest commit message on the main page
3. Click on "commits" to see the full history
4. Click on any commit to see the specific changes (files added/modified)

### Common Scenarios

#### Uploading a Complete Project Folder

If you have a project folder with multiple files:

```bash
# Copy your folder into the repository
cp -r /path/to/your-project-folder .

# Add everything in that folder
git add your-project-folder/

# Commit
git commit -m "Add complete project folder"

# Push
git push origin main
```

#### Updating Existing Files

```bash
# Make your changes to files
# Then check what changed
git status
git diff filename.py

# Add the modified files
git add filename.py

# Commit and push
git commit -m "Update filename.py with new feature"
git push origin main
```

#### Removing Files

```bash
# Remove a file from Git and your filesystem
git rm filename.txt
git commit -m "Remove unnecessary file"
git push origin main

# Remove a file from Git but keep it locally
git rm --cached filename.txt
git commit -m "Remove file from version control"
git push origin main
```

### Working with Branches

For larger changes, work on a separate branch:

```bash
# Create and switch to a new branch
git checkout -b feature-new-model

# Make your changes and commit
git add .
git commit -m "Add new detection model"

# Push the branch to GitHub
git push origin feature-new-model

# Later, merge into main via GitHub Pull Request
```

### Checking Your Upload Was Successful

After pushing, verify your changes:

```bash
# Fetch latest from GitHub
git fetch origin

# Compare your local branch with remote
git status

# See the commit history
git log --oneline -5
```

### Troubleshooting

#### Error: "fatal: remote origin already exists"
```bash
# Check your remote
git remote -v

# If wrong, remove and re-add
git remote remove origin
git remote add origin https://github.com/NiaFreeman/Picshield_Ai_Model.git
```

#### Error: "Your branch is behind"
```bash
# Pull the latest changes first
git pull origin main

# Then push your changes
git push origin main
```

#### Error: "Merge conflict"
```bash
# Pull and resolve conflicts
git pull origin main

# Edit conflicted files to resolve
# Then add and commit
git add .
git commit -m "Resolve merge conflicts"
git push origin main
```

### Best Practices

1. **Commit often**: Make small, frequent commits rather than large ones
2. **Write clear messages**: Describe what changed and why
3. **Pull before push**: Always pull latest changes before pushing
4. **Review changes**: Use `git diff` to review before committing
5. **Use .gitignore**: Don't commit temporary files, credentials, or large data files

### Useful Git Commands Reference

```bash
# View status
git status

# View changes
git diff
git diff filename.py
git diff --staged

# View history
git log
git log --oneline
git log --graph --all

# Undo changes (before commit)
git checkout -- filename.py

# Undo last commit (keep changes)
git reset --soft HEAD~1

# View remote repository info
git remote -v

# Update from remote
git pull origin main
git fetch origin
```

### Next Steps

1. Add your AI model files to the repository
2. Create a proper project structure (models/, data/, scripts/, etc.)
3. Add a requirements.txt for Python dependencies
4. Document your model architecture and usage
5. Add example code and datasets (if appropriate)

For more help with Git, visit: https://git-scm.com/doc
