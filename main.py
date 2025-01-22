from db_manager import DatabaseManager
from film_searcher import FilmSearcher
from console_interface import ConsoleInterface
from dotenv import load_dotenv

load_dotenv()


def main():
    db_manager = None
    try:
        db_manager = DatabaseManager()
    except Exception as e:
        print(f"Error connecting to the database: {e}")
    else:
        print("Successfully connected to the database.")
        film_searcher = FilmSearcher(db_manager)
        interface = ConsoleInterface(film_searcher)
        interface.run()

    finally:
        if db_manager:
            db_manager.close()


if __name__ == "__main__":
    main()
