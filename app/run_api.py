import os
import uvicorn


def main():
    """Run the FastAPI application with uvicorn."""
    host = os.getenv("API_HOST", "127.0.0.1")
    port = int(os.getenv("API_PORT", "8000"))
    
    uvicorn.run(
        "app.api.app:app",
        host=host,
        port=port,
        reload=True,
    )


if __name__ == "__main__":
    main()

