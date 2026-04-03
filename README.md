# ACEest Fitness & Gym 

A Flask-based web application and automated CI/CD pipeline built for the ACEest Fitness & Gym platform. This project demonstrates end-to-end DevOps practices — version control, containerisation, unit testing, and automated pipelines via GitHub Actions and Jenkins.

---

## Project Structure

```
.
├── app.py                        # Flask application entry point
├── src/
│   └── Aceestver.py              # Core business logic & program data
├── tests/
│   └── test_app.py               # Pytest unit tests
├── Dockerfile                    # Container image definition
├── pytest.ini                    # Pytest configuration
├── requirements.txt              # Python dependencies
├── Jenkinsfile                   # Jenkins declarative pipeline
└── .github/
    └── workflows/
        └── main.yml              # GitHub Actions CI/CD workflow
```

---

## Local Setup & Execution

**Prerequisites:** Python 3.12+, pip, Docker

```bash
# 1. Clone the repository
git clone <repo-url>
cd devops-assignment

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the Flask application
python app.py
```

The app will be available at `http://localhost:5000`.

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Home page (HTML) |
| GET | `/health` | Health check |
| GET | `/api/programs` | List all fitness programs |
| GET | `/api/programs/<code>` | Get program details (FL, MG, BG) |

---

## Running Tests Manually

```bash
# Run pytest from the project root
pytest -v
```

Tests cover the business logic in `src/Aceestver.py` and all Flask API endpoints in `app.py`.

### Running Tests Inside Docker

```bash
# Build the image
docker build -t aceest-fitness .

# Run pytest inside the container
docker run --rm aceest-fitness pytest -v
```

---

## CI/CD Pipeline Overview

### GitHub Actions (`.github/workflows/main.yml`)

Triggered on every **push** or **pull request** to `release-*` and `main` branches.

| Stage | What it does |
|-------|-------------|
| **Compile & Lint** | `python -m compileall` + `ruff check` for syntax and style errors |
| **Unit Tests** | Runs `pytest` against the source |
| **Docker Build** | Builds the container image tagged with the commit SHA |
| **Docker Test** | Runs `pytest` inside the built container to confirm environment consistency |
| **Release Build** | Triggered only on merge to `main` — builds the final release-tagged image |

### Jenkins (`Jenkinsfile`)

The Jenkins pipeline pulls the latest code from GitHub and runs a clean build. Stages:

1. **Checkout** — pulls source from the configured SCM (GitHub)
2. **Setup Environment** — creates a Python venv and installs dependencies
3. **Lint & Build Validation** — compiles source files and runs `ruff` linting
4. **Unit Tests** — executes `pytest` and publishes a JUnit XML report
5. **Docker Build** — builds the Docker image tagged with the Jenkins build number

> Jenkins acts as a secondary quality gate — validating that code integrates and builds correctly in a clean, controlled environment independent of the developer's machine.

---

## Branch Strategy

| Branch | Purpose |
|--------|---------|
| `main` | Stable, production-ready code. Merge triggers the release build. |
| `release-*` | Release-specific branches cut from `main`. All changes for a release are committed here. CI runs on every push. |

