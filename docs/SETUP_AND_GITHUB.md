# Setup and private GitHub connection

## 1. Preserve old files

Close VS Code. Use File Explorer to copy your original `C:\Development\Projects\Python_Art_Gallery_Maa_Kali` to `C:\Development\Backups\Python_Art_Gallery_Maa_Kali_old` (or choose a new backup name). Then **rename or move the old project folder out of `Projects`** so the cleaned folder can use the same name. Leave `Mitratics_Kali_Puja_Python_Starter` alone.

## 2. Extract the final ZIP

Extract the bundled top-level `Python_Art_Gallery_Maa_Kali` folder into `C:\Development\Projects\` so `render_radiant_31s.py` is directly inside the project folder. Avoid nested copies.

## 3. Verify it runs in VS Code Git Bash (UCRT64)

```bash
cd /c/Development/Projects/Python_Art_Gallery_Maa_Kali
PY="/c/Development/VirtualEnvironments/mitratics-kali-puja-python/Scripts/python.exe"
"$PY" --version
"$PY" -m pip install -r requirements.txt
bash run.sh test
bash run.sh preview
bash run.sh full
explorer.exe "$(cygpath -w output/Maa_Kali_Radiant_31s_Python.mp4)"
```

## 4. Create a private, empty repository on GitHub

In the GitHub website, choose New repository, name `python-art-gallery-maa-kali`, set **Private**, and do not initialize with README, license, or gitignore. Do not publish publicly without checking image and audio rights.

## 5. Initialize and connect via UCRT64 Git Bash

```bash
cd /c/Development/Projects/Python_Art_Gallery_Maa_Kali
git --version
git init
git branch -M main
git status
git add .
git status
git commit -m "Initial approved Maa Kali animation project"
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/python-art-gallery-maa-kali.git
git push -u origin main
```

Replace `YOUR_GITHUB_USERNAME` with your actual GitHub handle (not your display name or email). Sign in through your credential manager or the GitHub authorization prompt when requested. Do not put passwords or access tokens in commands or screenshots.

## 6. Verify

Visit the repository's Code tab; check `assets`, `code_art`, `tests`, `exports`, `.github/workflows`, and `render_radiant_31s.py`. Visit the Actions tab and confirm the Python tests workflow succeeds. Private status is visible near the repo name.

## 7. Ongoing development

```bash
git status
git add .
git commit -m "Describe change"
git push
```

If Git Bash reports an identity error, check `git config --global user.name` and `git config --global user.email`; you previously configured these on your machine.
