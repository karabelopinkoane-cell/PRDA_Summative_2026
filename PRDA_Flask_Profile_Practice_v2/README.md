# PRDA Flask Profile Practice v2

A classroom-ready Flask project for practising the PRDA application lifecycle.

## Features
- Home page and navigation
- User registration
- Input validation
- JSON storage
- Dynamic profile display
- Classroom login using Flask sessions
- Profile updates with preloaded values
- Profile list
- Automated Pytest tests
- Git-ready project structure
- Render deployment files

> The username-only login is deliberately simplified for classroom practice. It is not intended to demonstrate production authentication.

## Local setup on Windows
```powershell
python -m venv venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000

## Test locally
```powershell
pytest -v
```

## Git
```powershell
git init
git add .
git commit -m "Build PRDA Flask profile practice app"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

## Render
Build command:
```text
pip install -r requirements.txt
```
Start command:
```text
gunicorn app:app
```
Set a `SECRET_KEY` environment variable or deploy from the included `render.yaml`.

## Verify
- Home loads
- Register works
- Validation works
- Profile displays
- Login works
- Edit works
- `/health` returns `{"status":"ok"}`

## Important JSON note
This app uses JSON because it is easy to understand for classroom practice. On many cloud platforms, local files are not durable persistent storage after restarts or redeploys. For production, use persistent storage or a managed database.
