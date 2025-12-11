from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import api_v1_router

app = FastAPI(
    title="ToDoList API",
    description="""
A RESTful API for managing projects and tasks.

## Features

* **Projects**: Create, list, and delete projects
* **Tasks**: Add tasks to projects, update status, and manage deadlines
* **Validation**: Automatic input/output validation with Pydantic
* **Documentation**: Auto-generated OpenAPI documentation

## Architecture

This API follows a layered architecture:
- **Controllers** (Routes): Handle HTTP requests/responses
- **Services**: Business logic and validation
- **Repositories**: Database operations
- **Models**: SQLAlchemy ORM models
    """,
    version="0.3.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(api_v1_router)


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint - API health check."""
    return {
        "message": "ToDoList API is running",
        "version": "0.3.0",
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.get("/health", tags=["Root"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
