# PlacementAI

PlacementAI is an AI-powered application that analyses a CV, searches for suitable placement and internship vacancies, ranks them based on the candidate's profile, and emails newly discovered job matches.

## Features

- Analyses PDF/DOCX CVs
- Extracts skills, education, projects and experience using AI agents
- Searches live vacancies using the Adzuna API
- Ranks jobs based on CV suitability
- Filters unsuitable and duplicate vacancies
- Emails new matching jobs
- Automatically searches periodically while the backend is running

## Technologies

- Python
- FastAPI
- Ollama
- Adzuna Jobs API
- APScheduler
- Gmail SMTP

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/MusabBaig123/PlacementAI.git
cd PlacementAI/backend
```

The repository is private, so your GitHub account must have access.

### 2. Create and activate a virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create `backend/.env` using `.env.example` as a guide.

Add your own Adzuna API credentials and Gmail App Password.

Never commit the real `.env` file to GitHub.

### 5. Install and run Ollama

Install Ollama and ensure the model configured in:

```text
backend/app/agents/ollama_client.py
```

is available.

### 6. Start PlacementAI

From the `backend` folder:

```bash
python -m uvicorn main:app --reload
```

Then open:

```text
http://127.0.0.1:8000/docs
```

## Usage

Use the Swagger interface to:

1. `POST /cv/analyse-folder` — analyse a CV.
2. `GET /jobs/search` — find and rank matching vacancies.
3. `POST /jobs/test-email` — test email notifications.
4. `POST /jobs/search-and-notify` — find and email new matches.

The automatic scheduler searches for new vacancies while the backend is running.

## Security

Passwords, API keys, CV data, virtual environments and the local job database are excluded from GitHub through `.gitignore`.