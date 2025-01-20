from db_manager import DatabaseManager
from film_searcher import FilmSearcher
from console_interface import ConsoleInterface


def main():
    db_manager = DatabaseManager()
    film_searcher = FilmSearcher(db_manager)
    interface = ConsoleInterface(film_searcher)

    try:
        interface.run()
    finally:
        db_manager.close()


if __name__ == "__main__":
    main()
