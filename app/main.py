
import sys

from app.cli.console import ToDoListCLI
from app.db.session import SessionLocal


def main() -> None:
    """Run the ToDoList CLI application."""
    session = SessionLocal()
    session.commit()
    try:
        cli = ToDoListCLI(session)
        cli.run()
    except KeyboardInterrupt:
        print("\nExiting...")
        session.rollback()
    except Exception as e:
        session.rollback()

        print(f"Error: {e}")
        sys.exit(1)
    finally:
        session.close()


if __name__ == "__main__":
    main()

