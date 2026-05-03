# saca
Adaptive Clinical Assistant (SACA) for Remote Indigenous Communities

## Installation and Setup

This project uses a Python FastAPI backend, machine learning/NLP modules, and a PySide6 desktop frontend.

### 1. Recommended Python version

Use **Python 3.11 or 3.12** for best compatibility.

Python 3.13 may work for most of the project, but some packages, especially `PyAudio`, can be harder to install depending on your system.

Check your Python version:

```bash
python --version
```

### 2. Create a virtual environment

From the project root folder:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```bash
.\.venv\Scripts\Activate.ps1
```

Activate it on Windows Command Prompt:

```bash
.\.venv\Scripts\activate.bat
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Upgrade pip

```bash
python -m pip install --upgrade pip setuptools wheel
```

### 4. Install the project requirements

```bash
pip install -r requirements.txt
```

### 5. PyAudio installation note

`PyAudio` is required for microphone/voice input through `SpeechRecognition`.

If this command fails:

```bash
pip install PyAudio
```

try one of the following fixes.

#### Option A: Install Microsoft C++ Build Tools

Install Microsoft C++ Build Tools, then run:

```bash
pip install PyAudio
```

#### Option B: Use pipwin on Windows

```bash
pip install pipwin
pipwin install pyaudio
```

If voice input is not needed, the rest of the application can still be tested without PyAudio, but the voice recording page may not work.

### 6. Run the backend API

Open a terminal, activate the virtual environment, then run:

```bash
cd backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

The backend should now be running at:

```text
http://127.0.0.1:8000
```

### 7. Run the desktop frontend

Open a second terminal, activate the same virtual environment, then run:

```bash
cd frontend
python main.py
```

Make sure the backend is running before testing predictions from the frontend.

### 8. Optional: Train or compare ML models

From the project root or backend folder, run the relevant model script, for example:

```bash
cd backend
python ml/models/logistic_regression.py
python ml/models/linear_svc.py
python ml/models/naive_bayes.py
python ml/models/compare_models.py
```

For DistilBERT training:

```bash
cd backend
python ml/models/train_distilbert.py
```

DistilBERT training requires more disk space, RAM, and installation time because it uses `torch`, `transformers`, `datasets`, `evaluate`, and `accelerate`.

### 9. Common setup problems

#### `ModuleNotFoundError`

Make sure the virtual environment is activated and the requirements were installed:

```bash
pip install -r requirements.txt
```

#### Backend cannot find saved model files

Make sure the trained model files exist in the expected saved-model folder. If they are missing, run the relevant training script first.

#### Frontend cannot connect to backend

Make sure the FastAPI backend is running on:

```text
http://127.0.0.1:8000
```

Then restart the frontend.

