# Git Workflow Quick Reference

## Daily Workflow: Showing Your New Changes

### The Basic Cycle (Most Common)

```bash
# 1. See what changed
git status

# 2. Add your changes
git add .

# 3. Commit with a message
git commit -m "Description of what you changed"

# 4. Upload to GitHub
git push origin main
```

### Before You Start Working

```bash
# Make sure you have the latest code
git pull origin main
```

### To View Your Changes

#### See what files changed:
```bash
git status
```

#### See detailed line-by-line changes:
```bash
git diff                  # Changes not yet staged
git diff --staged         # Changes staged for commit
git diff HEAD            # All changes (staged and unstaged)
```

#### See specific file changes:
```bash
git diff filename.py
```

#### See commit history:
```bash
git log                  # Full history
git log --oneline        # Compact view
git log -3               # Last 3 commits
```

### Common Tasks

#### Add a New Folder
```bash
git add folder-name/
git commit -m "Add new folder with [description]"
git push origin main
```

#### Add Specific Files
```bash
git add file1.py file2.py file3.txt
git commit -m "Add [description]"
git push origin main
```

#### Update Existing Files
```bash
# Edit your files, then:
git add .
git commit -m "Update [description]"
git push origin main
```

#### Delete Files
```bash
git rm filename.txt
git commit -m "Remove [filename] because [reason]"
git push origin main
```

### Viewing Changes on GitHub

After pushing, go to:
- **Main page**: https://github.com/NiaFreeman/Picshield_Ai_Model
- **Commits**: https://github.com/NiaFreeman/Picshield_Ai_Model/commits
- **Compare**: https://github.com/NiaFreeman/Picshield_Ai_Model/compare

### Working on a New Feature

```bash
# Create a new branch for your feature
git checkout -b new-feature-name

# Make changes, then:
git add .
git commit -m "Add new feature"
git push origin new-feature-name

# Go to GitHub and create a Pull Request
```

### If Something Goes Wrong

#### Undo changes before commit:
```bash
git checkout -- filename.py    # Undo changes to one file
git reset --hard              # Undo all changes (careful!)
```

#### Undo last commit (keep changes):
```bash
git reset --soft HEAD~1
```

#### Undo last commit (discard changes):
```bash
git reset --hard HEAD~1
```

#### If push is rejected:
```bash
# Pull latest changes first
git pull origin main

# If there are conflicts, resolve them, then:
git add .
git commit -m "Merge remote changes"
git push origin main
```

### Checking Everything Is Uploaded

```bash
# Check if local matches remote
git status                    # Should say "nothing to commit, working tree clean"
git fetch origin             # Get latest info from GitHub
git status                   # Should say "Your branch is up to date"
```

### Essential Commands Cheat Sheet

| Command | Purpose |
|---------|---------|
| `git status` | See what changed |
| `git diff` | See detailed changes |
| `git add .` | Stage all changes |
| `git commit -m "message"` | Save changes with message |
| `git push origin main` | Upload to GitHub |
| `git pull origin main` | Download from GitHub |
| `git log` | See commit history |
| `git branch` | List branches |
| `git checkout -b name` | Create new branch |

### Tips

- ✅ **DO**: Commit often with clear messages
- ✅ **DO**: Pull before you push
- ✅ **DO**: Review changes with `git diff` before committing
- ❌ **DON'T**: Commit large binary files or sensitive data
- ❌ **DON'T**: Use `git push --force` (unless you know what you're doing)

## Visual Workflow

```
Your Computer                          GitHub
     |                                    |
     |-- 1. Make changes to files         |
     |                                    |
     |-- 2. git add .                     |
     |      (stage changes)               |
     |                                    |
     |-- 3. git commit -m "message"       |
     |      (save locally)                |
     |                                    |
     |-- 4. git push origin main ----------> Changes uploaded!
     |                                    |
     |                                    |-- Now visible on GitHub
     |                                    |
```

## Need More Help?

- See the main README.md for detailed explanations
- Visit: https://git-scm.com/docs
- GitHub Guide: https://guides.github.com/
