# 🤖 AI Resume Screening System — Complete Beginner Guide

---

## 📁 Project Structure
```
resume_screener/
│
├── app.py              ← Main server (Flask + AI logic)
├── requirements.txt    ← Python packages to install
├── templates/
│   └── index.html      ← The web interface (UI)
└── uploads/            ← Temporary folder (auto-created)
```

---

## 🔧 STEP 1 — Install Python

If you don't have Python yet:
- Go to https://www.python.org/downloads/
- Download **Python 3.10 or newer**
- During installation ✅ **check "Add Python to PATH"**

Verify it works — open a terminal/command prompt and type:
```
python --version
```
You should see something like `Python 3.11.4`

---

## 🔑 STEP 2 — Get Your Anthropic API Key

1. Go to https://console.anthropic.com/
2. Sign up / Log in
3. Click **"API Keys"** in the left sidebar
4. Click **"Create Key"** → copy the key (starts with `sk-ant-...`)

> ⚠️ Keep this key secret! Never share it or commit it to GitHub.

---

## 🖥️ STEP 3 — Set Your API Key as an Environment Variable

**On Mac/Linux** — open Terminal and run:
```bash
export ANTHROPIC_API_KEY="sk-ant-YOUR_KEY_HERE"
```

**On Windows** — open Command Prompt and run:
```cmd
set ANTHROPIC_API_KEY=sk-ant-YOUR_KEY_HERE
```

Or on Windows PowerShell:
```powershell
$env:ANTHROPIC_API_KEY = "sk-ant-YOUR_KEY_HERE"
```

> 💡 Tip: To make it permanent on Windows, search "Environment Variables" in Start Menu and add it there.

---

## 📦 STEP 4 — Install Required Packages

Open a terminal, navigate to your project folder, then run:

```bash
cd resume_screener
pip install -r requirements.txt
```

This installs:
- **flask** — the web server
- **PyPDF2** — reads PDF files
- **anthropic** — connects to Claude AI

---

## ▶️ STEP 5 — Run the App

```bash
python app.py
```

You should see:
```
✅ AI Resume Screener is running!
   Open http://127.0.0.1:5000 in your browser
```

---

## 🌐 STEP 6 — Use the App

1. Open your browser and go to: **http://127.0.0.1:5000**
2. Paste a **job description** in the text box
3. Click **"click to browse"** or drag & drop **PDF resumes**
4. Click **"🚀 Screen Resumes with AI"**
5. Wait a few seconds — results appear ranked by match score!

---

## 🧠 How It Works (Simple Explanation)

```
You upload PDFs  →  PyPDF2 extracts the text  →  Claude AI reads
the resume text + job description  →  Claude returns a score (0-100),
skills list, strengths, gaps  →  Flask sends it to your browser  →
Results displayed ranked best to worst
```

---

## 📊 What the Results Show

| Field | What it means |
|-------|---------------|
| **Match Score** | 0–100% — how well the resume fits the job |
| **Skills Detected** | Programming languages, tools, soft skills found |
| **Strengths** | Why this candidate is a good fit |
| **Gaps** | What's missing compared to the job description |
| **Match Reason** | A one-sentence AI summary |

---

## 🛠️ Troubleshooting

### "ModuleNotFoundError: No module named 'flask'"
Run: `pip install -r requirements.txt`

### "AuthenticationError" or API key error
Make sure you set the environment variable correctly (Step 3).
Double-check the key has no spaces around it.

### "Could not extract text from this PDF"
The PDF is probably scanned (image-based). You'd need OCR (e.g., pytesseract).
Try a different PDF that has selectable text.

### Port already in use
Change the port at the bottom of app.py:
```python
app.run(debug=True, port=5001)
```

---

## 🚀 Optional Improvements (When You're Ready)

- **Add a database** — save results with SQLite
- **Export to Excel** — use pandas to export candidate rankings
- **Add login** — use Flask-Login to protect the app
- **Deploy online** — use Railway.app or Render.com (free hosting)
- **OCR support** — use pytesseract for scanned PDFs

---

## 💰 API Cost Estimate

Each resume analysis uses roughly **500–1500 tokens**.
- Claude Opus 4.6: ~$0.01–0.04 per resume
- Screening 50 resumes ≈ $0.50–$2.00 total

---

## 🆘 Need Help?

- Anthropic Docs: https://docs.anthropic.com
- Flask Docs: https://flask.palletsprojects.com
- PyPDF2 Docs: https://pypdf2.readthedocs.io
