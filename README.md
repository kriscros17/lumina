# ✦ Lumina — A Wellness & Soul Journal

A vintage-styled personal wellness oracle built with Python (Flask) and HTML/CSS/JS.
Six sections. All features. Zero external database needed.

---

## ✦ Features

| Section | What It Does |
|---|---|
| **I. Wellness** | 7 sliders → weighted score → 6 mood states → colour palette + element + breathing |
| **II. Personality** | 20 questions → MBTI + DISC + Temperament scored simultaneously |
| **III. Your Reading** | Full accordion profiles for all three systems + ideal partner synthesis |
| **IV. Gratitude Journal** | Write & save 3 daily gratitude entries (persists in session) |
| **V. Moon Phase** | Live lunar calendar with illumination + wellness context |
| **VI. Colour Therapy** | Psychology of 6 colour spectrums for mood regulation |

---

## 🚀 Setup on MacBook Air M4 + VSCode — 8 Steps

### Step 1 — Check Python is installed
```bash
python3 --version
```
If not installed, install Homebrew then Python:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python
```

---

### Step 2 — Open the project folder in VSCode
```bash
cd ~/Downloads/lumina2    # or wherever you unzipped it
code .
```
Or: **File → Open Folder** in VSCode → select the `lumina2` folder.

---

### Step 3 — Open the integrated terminal
**Ctrl + `` ` ``** (backtick key, top-left of keyboard)

---

### Step 4 — Create a virtual environment
```bash
python3 -m venv venv
```
A `venv/` folder appears in the sidebar.

---

### Step 5 — Activate the virtual environment
```bash
source venv/bin/activate
```
You'll see `(venv)` at the start of your terminal prompt.

---

### Step 6 — Install Flask
```bash
pip install -r requirements.txt
```

---

### Step 7 — Run the app
```bash
python app.py
```
Expected output:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

---

### Step 8 — Open in your browser
**http://127.0.0.1:5000**

---

## 🛑 Stop the server
Press **Ctrl + C** in the terminal.

---

## 🔁 Next time
```bash
source venv/bin/activate
python app.py
```

---

## 📁 Project Structure
```
lumina2/
├── app.py              ← Python backend (all logic + all data)
├── requirements.txt    ← Just: flask==3.0.3
├── templates/
│   └── index.html      ← Complete frontend (HTML + CSS + JS)
└── README.md
```

---

## 🧠 How the Python Code Works — For Beginners
The `app.py` file is thoroughly annotated with plain-English explanations of every
concept: imports, dictionaries, functions, loops, Flask routes, HTTP methods,
session storage, and the moon phase calculation formula.

Open `app.py` in VSCode and read through it — every section is explained.

Key concepts covered:
- What `import` does
- What a Python dictionary `{}` is
- What `def` and `return` do (functions)
- How `for` loops work
- What Flask routes `@app.route()` do
- What `GET` vs `POST` means in HTTP
- How `session` stores user data
- How the moon phase formula works mathematically

---

> 💙 Lumina is not a substitute for professional mental health support.
> If you are struggling, please reach out to a qualified professional or someone you trust.
