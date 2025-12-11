# ToDoList - RESTful API with FastAPI

A ToDoList manager with a RESTful API built using FastAPI, featuring PostgreSQL database persistence, layered architecture, and scheduled task automation.


**Migration Path:**
1. Start the API server (see usage below)
2. Use the interactive API documentation at http://localhost:8000/docs
3. Integrate your applications with the RESTful endpoints

## Features

RESTful API with FastAPI – Full CRUD for Projects & Tasks
Everything you expect from a proper backend is here:

Create, read, update, delete projects and tasks
All endpoints follow REST conventions (proper HTTP verbs, status codes, URLs)
JSON in → JSON out, exactly like big APIs (GitHub, Stripe, Twitter, etc.)

Auto interactive documentation – Swagger UI & ReDoc
As soon as you run the server, you get two beautiful, auto-updated docs sites for free:

http://localhost:8000/docs → Swagger UI (try buttons, you can test every endpoint directly in the browser
http://localhost:8000/redoc → cleaner alternative documentation
No need to write Postman collections or separate docs ever again.

Pydantic validation – Strict request/response schemas
Every piece of data that comes in or goes out is automatically checked by Pydantic models:

Wrong type? → instant 422 error with clear message
Missing required field? → instant error
Invalid date format? → instant error
Your database is protected from garbage data 100% of the time.

Layered Architecture – API → Service → Repository → SQLAlchemy Models
The code is split into very clear layers so it never becomes spaghetti:

Routes (API layer) → only talk to Services
Services → contain all business rules (e.g., “a project can’t have more than 100 tasks”)
Repositories → only talk to the database, nothing else
Models → pure SQLAlchemy table definitions
Result: you can test everything in isolation and the project stays clean even when it grows huge.

Dependency Injection – Constructor injection everywhere
Every class gets what it needs through the constructor (exactly like we talked about earlier with the robot and its arms).
Because of this, unit tests are extremely easy – you just pass fake repositories.
FastAPI’s Depends() does all the magic automatically.
PostgreSQL + Alembic migrations
Real production database (not SQLite) + proper migration system:

You can evolve the schema safely over years
Roll back if something goes wrong
Zero-downtime migrations in production

Overdue task auto-closure
If a task has a deadline and the date passes while status is still “todo” or “doing”, a background command automatically sets it to “done (overdue)”.
You can run it manually or let the built-in scheduler run it every 15 minutes.
Rate limiting per user / per project
Built-in protection against abuse:

Configurable max number of projects per user
Max number of tasks per project
Trying to create more → polite 400 error instead of letting the database explode.

CORS & security headers
Ready to be consumed by any frontend (React, Vue, Svelte, mobile apps):

CORS is configurable (default allows everything in dev, you tighten it in prod)
FastAPI automatically adds correct security headers

Docker-ready PostgreSQL
One single command starts a real PostgreSQL instance that survives computer restarts:
docker run --name todolist-postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:16
(or even better, the docker-compose version I gave you).
Poetry for dependency management
No more “it works on my machine” problems:

pyproject.toml + poetry.lock = exactly the same packages and versions for everyone
poetry install and you’re ready in seconds
Dev dependencies (pytest, black, mypy) are separated from production ones

In short: this little ToDoList project is built exactly like a serious production backend in 2025 – small, simple, but using every modern best practice so it can grow into a huge system without ever needing a painful refactor.
That’s why it’s perfect both for learning and for using as a real-world starter template.

## Architecture

This project follows a layered architecture with clear separation of concerns:

- **API Layer** (`app/api/`): FastAPI routes and request/response handling
- **Service Layer** (`app/services/`): Business logic and validation
- **Repository Layer** (`app/repositories/`): Database operations (CRUD)
- **Models** (`app/models/`): SQLAlchemy ORM models
- **Schemas** (`app/api/v1/schemas/`): Pydantic models for validation

## Project Structure

```
├── app/                    # Main application package
│   ├── api/               # FastAPI application
│   │   ├── v1/           # API version 1
│   │   │   ├── routes/   # API endpoints
│   │   │   └── schemas/  # Pydantic models
│   │   └── app.py        # FastAPI app initialization
│   ├── cli/               # [DEPRECATED] Command Line Interface
│   │   └── console.py    # CLI implementation
│   ├── commands/          # Scheduled task commands
│   │   ├── autoclose_overdue.py
│   │   └── scheduler.py
│   ├── db/                # Database configuration
│   │   ├── base.py       # SQLAlchemy Base
│   │   └── session.py    # Database session management
│   ├── exceptions/        # Custom exceptions
│   │   ├── base.py
│   │   ├── repository_exceptions.py
│   │   └── service_exceptions.py
│   ├── models/            # SQLAlchemy ORM models
│   │   ├── project.py
│   │   └── task.py
│   ├── repositories/      # Repository pattern implementation
│   │   ├── project_repository.py
│   │   └── task_repository.py
│   ├── services/          # Business logic layer
│   │   ├── project_service.py
│   │   └── task_service.py
│   └── main.py            # CLI entry point (deprecated)
├── alembic/               # Database migrations
├── .env.example           # Environment variables template
├── pyproject.toml         # Poetry dependencies
└── poetry.lock            # Poetry lock file
```

## Prerequisites

- Python 3.10+
- Docker Desktop (for PostgreSQL)
- Poetry

## Setup

### 1. Install Dependencies

```bash
poetry install
```

### 2. Set Up PostgreSQL with Docker

```bash
docker run --name todolist-postgres -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=todolist -p 5432:5432 -d postgres:16
```

### 3. Configure Environment Variables

Copy the example environment file and adjust as needed:

```bash
cp .env.example .env
```

The `.env` file should contain:
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/todolist
MAX_NUMBER_OF_PROJECTS=10
MAX_NUMBER_OF_TASKS_PER_PROJECT=100

# API Server Configuration (optional)
API_HOST=127.0.0.1  # Use 0.0.0.0 to allow external connections (security risk - use with caution)
API_PORT=8000
API_ENV=development  # Set to 'production' to disable auto-reload

# CORS Configuration
CORS_ORIGINS=*  # Use specific domains in production
```

### 4. Run Database Migrations

```bash
poetry run alembic upgrade head
```

## Usage

### Run the REST API (Recommended)

Start the API server:
```bash
poetry run todolist-api
```

Alternatively, you can run uvicorn directly:
```bash
poetry run uvicorn app.api.app:app --reload
```

The API will be available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **API endpoints**: http://localhost:8000/api/v1/

#### API Endpoints

**Projects:**
- `POST /api/v1/projects/` - Create a new project
- `GET /api/v1/projects/` - List all projects
- `GET /api/v1/projects/{project_id}` - Get a specific project
- `DELETE /api/v1/projects/{project_id}` - Delete a project

**Tasks:**
- `POST /api/v1/projects/{project_id}/tasks/` - Create a new task
- `GET /api/v1/projects/{project_id}/tasks/` - List all tasks in a project
- `GET /api/v1/projects/{project_id}/tasks/{task_id}` - Get a specific task
- `PATCH /api/v1/projects/{project_id}/tasks/{task_id}/status` - Update task status
- `DELETE /api/v1/projects/{project_id}/tasks/{task_id}` - Delete a task

### Run the CLI (Deprecated)

⚠️ **Warning**: The CLI is deprecated. Please use the REST API instead.

```bash
poetry run todolist
```

### Auto-close Overdue Tasks

Run manually:
```bash
poetry run todolist-autoclose
```

Or use the scheduler (runs every 15 minutes):
```bash
poetry run todolist-scheduler
```

### Set Up as Cron Job

Add to your crontab (runs every 15 minutes):
```bash
*/15 * * * * cd /path/to/project && poetry run todolist-autoclose
```

## Development

### Create a New Migration

After modifying models:
```bash
poetry run alembic revision --autogenerate -m "Description of changes"
```

### Apply Migrations

```bash
poetry run alembic upgrade head
```

### Rollback Migration

```bash
poetry run alembic downgrade -1
```

## API Examples

### Create a Project

```bash
curl -X POST "http://localhost:8000/api/v1/projects/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Project",
    "description": "A detailed description of my project"
  }'
```

### Create a Task

```bash
curl -X POST "http://localhost:8000/api/v1/projects/1/tasks/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete Phase 3",
    "description": "Implement FastAPI endpoints",
    "deadline": "2025-12-31T23:59:59"
  }'
```

### Update Task Status

```bash
curl -X PATCH "http://localhost:8000/api/v1/projects/1/tasks/1/status" \
  -H "Content-Type: application/json" \
  -d '{"status": "doing"}'
```

### List All Projects

```bash
curl http://localhost:8000/api/v1/projects/
```

## Migration from CLI to API

The CLI has been deprecated in favor of the REST API. Here's how CLI operations map to API endpoints:

| CLI Operation | API Endpoint |
|---------------|--------------|
| List projects | `GET /api/v1/projects/` |
| Create project | `POST /api/v1/projects/` |
| Delete project | `DELETE /api/v1/projects/{id}` |
| List tasks | `GET /api/v1/projects/{id}/tasks/` |
| Add task | `POST /api/v1/projects/{id}/tasks/` |
| Change task status | `PATCH /api/v1/projects/{id}/tasks/{task_id}/status` |

## Architecture

This project follows a layered architecture:

- **API Routes**: Handle HTTP requests/responses (FastAPI)
- **Services**: Business logic and validation
- **Repositories**: Handle all database operations (CRUD)
- **Models**: SQLAlchemy ORM models representing database tables
- **Schemas**: Pydantic models for request/response validation
- **Commands**: Background/scheduled tasks

Dependency Injection is used throughout to ensure loose coupling and testability.
