# 🐙 Step-by-Step Guide: How to Host Nikki on GitHub

Follow these simple steps to host Nikki on GitHub so you can access, clone, and run her anywhere!

---

## Step 1: Create a Repository on GitHub.com

1. Open your browser and go to [GitHub.com](https://github.com/). Sign in (or create a free account).
2. Click the **`+`** icon in the top right corner and click **New repository** (or visit [github.com/new](https://github.com/new)).
3. Fill in the details:
   - **Repository name**: `nikki-ai`
   - **Description**: `Nikki - Autonomous Local AI Assistant (Zero API Keys)`
   - **Public or Private**: Choose **Public** (or **Private** if you prefer).
   - **Initialize this repository with**: Leave **UNCHECKED** (do not add README or license, we already built them).
4. Click **Create repository**.

---

## Step 2: Push Nikki's Code to GitHub

Open Command Prompt or PowerShell on your computer and copy-paste these commands:

```cmd
:: 1. Navigate to Nikki's workspace folder
cd C:\Users\ABC\.gemini\antigravity\scratch\local_ai_assistant

:: 2. Initialize Git
git init

:: 3. Add all project files
git add .

:: 4. Create your first commit
git commit -m "Initial commit of Nikki Autonomous AI Assistant"

:: 5. Set default branch to main
git branch -M main

:: 6. Link to your GitHub repository (replace YOUR-USERNAME with your actual GitHub username)
git remote add origin https://github.com/YOUR-USERNAME/nikki-ai.git

:: 7. Push Nikki's code to GitHub!
git push -u origin main
```

---

## Step 3: Enable 24/7 Background Cloud Learning on GitHub Actions

1. Go to your GitHub repository page (`https://github.com/YOUR-USERNAME/nikki-ai`).
2. Click the **Actions** tab at the top.
3. Click **I understand my workflows, go ahead and enable them**.
4. Nikki will now automatically run 24/7 background learning cycles on free GitHub cloud servers every 6 hours and update her knowledge base!

---

## Step 4: Clone & Run Nikki Anywhere

Now you can install and run Nikki on any device with **one command**:

### On Android Phone (Termux):
```bash
pkg install git python -y
git clone https://github.com/YOUR-USERNAME/nikki-ai.git
cd nikki-ai
python main.py --voice
```

### On Windows PC / Laptop:
```cmd
git clone https://github.com/YOUR-USERNAME/nikki-ai.git
cd nikki-ai
start_nikki.bat
```
