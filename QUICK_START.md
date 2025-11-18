# Quick Start: Upload Your Folder in 3 Minutes

## The Fastest Way to Show Your Changes

### Step 1: Check What You Have
```bash
git status
```

### Step 2: Add Everything
```bash
git add .
```

### Step 3: Save Your Changes
```bash
git commit -m "Add my new work"
```

### Step 4: Upload to GitHub
```bash
git push origin main
```

## That's It! 🎉

Your changes are now on GitHub at:
https://github.com/NiaFreeman/Picshield_Ai_Model

---

## Example: Adding a New Folder

Let's say you have a folder called `my-model` with your AI model:

```bash
# 1. Copy your folder to the repository
# (Use your file manager or command line)
cp -r /path/to/my-model .

# 2. Add it to Git
git add my-model/

# 3. Save it
git commit -m "Add my-model folder with AI detection code"

# 4. Upload it
git push origin main
```

**Done!** View it on GitHub: https://github.com/NiaFreeman/Picshield_Ai_Model

---

## See Your Changes

### On Your Computer:
```bash
git status          # What changed?
git diff           # What's different?
git log            # What did I upload?
```

### On GitHub:
1. Go to: https://github.com/NiaFreeman/Picshield_Ai_Model
2. Click "commits" to see all changes
3. Click any commit to see details

---

## Common Questions

**Q: How do I know if it uploaded?**  
A: Run `git status`. If it says "nothing to commit, working tree clean" and "Your branch is up to date", it's uploaded!

**Q: What if I get an error?**  
A: Try pulling first: `git pull origin main`, then push again.

**Q: Can I add just one file?**  
A: Yes! Use `git add filename.py` instead of `git add .`

**Q: How do I undo changes?**  
A: Before commit: `git checkout -- filename.py`  
After commit: See CONTRIBUTING.md for details

---

## Need More Help?

- **Quick Commands**: See [GIT_WORKFLOW.md](GIT_WORKFLOW.md)
- **Detailed Guide**: See [README.md](README.md)
- **Contributing**: See [CONTRIBUTING.md](CONTRIBUTING.md)
