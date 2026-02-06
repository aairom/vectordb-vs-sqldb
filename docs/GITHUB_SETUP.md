# GitHub Setup Guide

This guide will help you push your project to GitHub.

## Prerequisites

- Git installed on your system
- A GitHub account (create one at https://github.com/signup if needed)

## Step-by-Step Instructions

### 1. Create a New Repository on GitHub

1. Go to https://github.com/new
2. Fill in the repository details:
   - **Repository name**: `vectordb-vs-sqldb` (or your preferred name)
   - **Description**: "Educational demonstration comparing traditional SQL databases with Vector Databases"
   - **Visibility**: Choose Public or Private
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
3. Click "Create repository"

### 2. Copy Your Repository URL

After creating the repository, GitHub will show you a URL like:
```
https://github.com/YOUR_USERNAME/vectordb-vs-sqldb.git
```

Copy this URL - you'll need it in the next step.

### 3. Push to GitHub Using the Automation Script

Now you can use the automation script with your repository URL:

```bash
cd /Users/alainairom/Devs/vectordb-vs-sqldb
./scripts/push_to_github.sh https://github.com/YOUR_USERNAME/vectordb-vs-sqldb.git
```

**Replace `YOUR_USERNAME` with your actual GitHub username!**

The script will:
- Initialize git repository (if needed)
- Configure the remote repository
- Check for uncommitted changes
- Stage all changes
- Prompt you for a commit message
- Push to GitHub
- Display the repository URL

**Alternative**: If you run the script without arguments, it will prompt you to enter the URL:

```bash
./scripts/push_to_github.sh
# Then enter your URL when prompted
```

## Manual Push (Alternative Method)

If you prefer to push manually:

```bash
# Stage all changes
git add .

# Commit with a message
git commit -m "Initial commit: Vector DB vs SQL DB comparison app"

# Push to GitHub
git push -u origin main
```

## Troubleshooting

### Error: "remote origin already exists"

If you see this error, remove the existing remote and add it again:

```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/vectordb-vs-sqldb.git
```

### Error: "failed to push some refs"

This usually means the remote repository has changes that you don't have locally. Try:

```bash
git pull origin main --rebase
git push -u origin main
```

### Authentication Issues

GitHub no longer accepts password authentication. You need to use:

1. **Personal Access Token (PAT)**:
   - Go to https://github.com/settings/tokens
   - Generate new token (classic)
   - Select scopes: `repo` (full control of private repositories)
   - Copy the token and use it as your password when prompted

2. **SSH Keys** (recommended):
   - Generate SSH key: `ssh-keygen -t ed25519 -C "your_email@example.com"`
   - Add to SSH agent: `ssh-add ~/.ssh/id_ed25519`
   - Add public key to GitHub: https://github.com/settings/keys
   - Use SSH URL: `git@github.com:YOUR_USERNAME/vectordb-vs-sqldb.git`

### Changing Remote URL

To switch from HTTPS to SSH (or vice versa):

```bash
# View current remote
git remote -v

# Change to SSH
git remote set-url origin git@github.com:YOUR_USERNAME/vectordb-vs-sqldb.git

# Or change to HTTPS
git remote set-url origin https://github.com/YOUR_USERNAME/vectordb-vs-sqldb.git
```

## What Gets Pushed?

The `.gitignore` file ensures these items are NOT pushed to GitHub:

- `__pycache__/` - Python cache files
- `*.pyc`, `*.pyo`, `*.pyd` - Python compiled files
- `.Python` - Python environment
- `venv/`, `env/` - Virtual environments
- `*.db` - Database files
- `*.log` - Log files
- `.DS_Store` - macOS system files
- `_*/` - Any folder starting with underscore

## Subsequent Pushes

After the initial setup, you can use the automation script anytime:

```bash
./scripts/push_to_github.sh
```

Or manually:

```bash
git add .
git commit -m "Your commit message"
git push
```

## Viewing Your Repository

After pushing, visit:
```
https://github.com/YOUR_USERNAME/vectordb-vs-sqldb
```

You should see all your project files, documentation, and the README displayed on the main page.

## Best Practices

1. **Commit frequently** with meaningful messages
2. **Pull before push** if working with others: `git pull origin main`
3. **Review changes** before committing: `git status` and `git diff`
4. **Use branches** for new features: `git checkout -b feature-name`
5. **Keep sensitive data out** - never commit API keys, passwords, or tokens

## Need Help?

- GitHub Documentation: https://docs.github.com
- Git Documentation: https://git-scm.com/doc
- GitHub Support: https://support.github.com