
import sys

from app.cli.console import ToDoListCLI
from app.db.session import SessionLocal


def main() -> None:
    """Run the ToDoList CLI application."""
    session = SessionLocal()
    try:
        cli = ToDoListCLI(session)
        cli.run()
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        session.close()


if __name__ == "__main__":
    main()
