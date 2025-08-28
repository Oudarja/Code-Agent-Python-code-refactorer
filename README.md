# Dockerized Development & Common Commands

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Build and Run with Docker Compose

From the project root:

```bash
# Build all services
docker compose build

# Start all services
docker compose up

# Start in detached mode
docker compose up -d

# Stop all services
docker compose down
```

## Accessing the App

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

## Common Docker Commands

```bash
# Rebuild a specific service (e.g., frontend)
docker compose build frontend

# View logs for a service
docker compose logs frontend

# Restart a service
docker compose restart backend

# Remove all stopped containers, networks, images
docker system prune -a
```

## Development (without Docker)

You can still run backend and frontend separately for development:

```bash
# Backend
cd backend/app
uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```
# CodeAgent – AI-Powered Python Refactoring Assistant

**CodeAgent** is an AI developer assistant that analyzes, refactors, tests, and documents Python code directly from GitHub repositories. It uses powerful LLMs like **Groq's LLaMA 3 (70B)** to improve code quality, automate documentation, and boost developer productivity.

---

## Project Overview

This is a full-stack project consisting of:

- **Frontend**: Built with **Next.js** for user-friendly interaction  
- **Backend**: Powered by **FastAPI** and integrates Groq's LLMs  
- **LLM Logic**: Modular pipeline for analysis, refactoring, testing, and documentation  
- **GitHub Integration**: Analyze, update, and push changes directly to GitHub  

---

## Tech Stack

| Layer      | Technology                             |
|------------|-----------------------------------------|
| Frontend   | Next.js (App Router), Tailwind CSS |
| Backend    | Python, FastAPI                         |
| LLM API    | Groq `llama3-70b-8192`, `meta-llama/llama-4-scout-17b-16e-instruct` using `LangChain`                 |
| GitHub API | For file and repo access               |

---

## Project Structure

```
code-agent/
├── backend/                    # FastAPI backend
│   └── app/
│       ├── controller/         # FastAPI API route handlers
│       ├── models/             # Pydantic models and schema definitions
│       ├── services/           # GitHub integration and business logic
│       ├── tests/              # Backend unit and integration tests
│       ├── utils/              # LLM logic (refactoring, README, testing, etc.) and helper functions
│       └── .env                # Set environment variable
├── frontend/                   # Next.js frontend
│   ├── app/                    # App router structure (Next.js 13+ routing)
│   ├── components/             # React components (UI elements)
│   ├── context/                # React context providers (e.g. global state)
│   ├── lib/                    # API logic and client-side utilities
│   ├── public/                 # Static assets (images, icons, etc.)
│   └── .env.local              # Set environment variable

```

---

## Key Features

### Code Analyzer
- Detects outdated syntax, anti-patterns, hardcoded values, and maintainability issues.

### Code Refactorer
- Refactors legacy or modern code into idiomatic Python (`3.x`) using LLMs.

### Test Case Generator
- Creates `pytest`-compatible unit tests for refactored code.

### Documentation Generator
- Generates Pythonic docstrings, function/class/module-level documentation.

### Code Diff Viewer
- Side-by-side comparison of original vs refactored code.

### Requirements Updater
- Updates `requirements.txt` to latest compatible packages.

### README Generator
- Generates repo-level README summarizing all files and project structure.

### Runtime Validator
- Creates virtualenv, installs updated dependencies for validation.

### GitHub Integration
- Analyze GitHub repos and branches
- Refactor and push code to a new branch
- Create pull requests with title and description

---

## How to Run the Backend (FastAPI)

## Prerequisites

| Tool        | Version (Recommended) |
|-------------|------------------------|
| Python      | 3.12.6                  |
| Node.js     | 22.17.1 LTS            |
| npm         | Comes with Node        |
| Git         | Latest                 |

---

### 1. Clone & Navigate
```bash
git clone git@gitlab.com:cloudlyio/code-agent.git
cd code-agent
```
### 2. Set Environment Variables
Create a `.env` file to root `code-agend` folder:
```python
GROQ_API_KEY=your_groq_api_key
GITHUB_TOKEN=your_github_token
# GROQ_MODEL=llama3-70b-8192
GROQ_MODEL=meta-llama/llama-4-scout-17b-16e-instruct
GROQ_TEMPERATURE=0.3
GROQ_TOP_P=0.9
GROQ_MAX_COMPLETION_TOKENS=4096
NEXT_PUBLIC_API_BASE_URL=Your backend base api
```

### 3. Set Up Virtual Environment
```bash
cd .\backend\
python -m venv .ca
source .ca/Scripts/activate  
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```
### 5. Run the API Server
```bash
cd .\backend\app\
uvicorn main:app --reload
```

Backend will be available at:   `http://localhost:8000`

---

## How to Run the Frontend (Next.js)

### 1. Navigate to Frontend
```bash
cd ./frontend
```
### 2. Set environment variable
Create `.env.local` file
```python
NEXT_PUBLIC_API_BASE_URL = Your backend base api
```

### 3. Install Node.js Dependencies
```bash
npm install
```

### 4. Run Dev Server
```bash
npm run dev
```

Frontend will be available at:   `http://localhost:3000`

---

## Frontend Route Overview

| Path | Purpose |
|------|---------|
| `/` | Home / Repo Input |
| `/refactor` | Launch code refactoring |
| `/overview` | See repo summary and original codes |
| `/readme_generation` |Generate and View README |
| `/dependency_management` | Manage and update dependencies |
| `/github_action` | Commit and PR integration |
| `/analyzer` | Code analysis and observe refactored result |

---



