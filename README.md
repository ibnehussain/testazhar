# Mergington High School — Extracurricular Activities API

A lightweight FastAPI application that lets students at Mergington High School browse and sign up for extracurricular activities through a simple web interface.

## About

The app exposes a REST API backed by an in-memory activity store. A static HTML/CSS/JS front-end is served alongside the API, allowing students to:

- View all available extracurricular activities (name, description, schedule, capacity, and current participants)
- Sign up for an activity using their school email address

Activities currently offered: **Chess Club**, **Programming Class**, and **Gym Class**.

## Project Structure

```
testazhar/
├── pytest.ini                  # Pytest configuration
├── requirements.txt            # Python dependencies
├── src/
│   ├── app.py                  # FastAPI application and API routes
│   ├── static/
│   │   ├── index.html          # Main web page
│   │   ├── app.js              # Front-end JavaScript (fetches API, handles signup form)
│   │   └── styles.css          # Page styles
│   └── tests/
│       └── test_app.py         # API tests (pytest + FastAPI TestClient)
└── README.md
```

## Getting Started

### Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

- **Windows:** `.venv\Scripts\activate`
- **macOS/Linux:** `source .venv/bin/activate`

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the development server

```bash
uvicorn src.app:app --reload
```

Then open [http://localhost:8000](http://localhost:8000) in your browser.

### Run tests

```bash
pytest src/tests/test_app.py -v
```

## Deploy to Azure App Service

### Prerequisites

- Azure subscription
- [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)

### 1) Sign in and create Azure resources

```bash
az login
az group create --name merington-rg --location eastus
az appservice plan create --name merington-plan --resource-group merington-rg --sku B1 --is-linux
az webapp create --resource-group merington-rg --plan merington-plan --name <your-unique-app-name> --runtime "PYTHON:3.12"
```

### 2) Configure startup command

```bash
az webapp config set --resource-group merington-rg --name <your-unique-app-name> --startup-file "python -m uvicorn src.app:app --host 0.0.0.0 --port \$PORT"
```

### 3) Deploy the app code from this repository

```bash
zip -r app.zip . -x ".git/*" ".venv/*" "__pycache__/*" "*.pyc"
az webapp deploy --resource-group merington-rg --name <your-unique-app-name> --src-path app.zip --type zip
```

### 4) Open the deployed app

```bash
az webapp browse --resource-group merington-rg --name <your-unique-app-name>
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Redirects to the web UI |
| `GET` | `/activities` | Returns all activities and their details |
| `POST` | `/activities/{activity_name}/signup?email=...` | Signs a student up for an activity |

## Tech Stack

- **[FastAPI](https://fastapi.tiangolo.com/)** — API framework
- **[Uvicorn](https://www.uvicorn.org/)** — ASGI server
- **[pytest](https://pytest.org/)** — Test framework
