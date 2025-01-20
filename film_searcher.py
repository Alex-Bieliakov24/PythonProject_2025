from typing import List, Tuple
from db_manager import DatabaseManager

class FilmSearcher:
    """
    A class responsible for handling film search functionality.

    This class interacts with the database through the DatabaseManager to perform
    searches, log queries, and retrieve popular search queries.
    """

    def __init__(self, db_manager: DatabaseManager):
        """
        Initializes the FilmSearcher with a DatabaseManager instance.

        Parameters:
            db_manager (DatabaseManager): An instance of DatabaseManager to interact with the database.
        """
        self.db_manager = db_manager

    def log_query(self, query: str) -> None:
        """
        Logs a search query into the database.

        Parameters:
            query (str): The query text to be logged.

        Behavior:
            - Attempts to insert the query into the 'query_logs' table.
            - Prints an error message if the logging fails.
        """
        try:
            self.db_manager.execute_query(
                "INSERT INTO query_logs (query_text) VALUES (%s)", (query,)
            )
        except Exception as e:
            print(f"Error logging the query: {e}")

    def search_by_keyword(self, keyword: str) -> List[Tuple]:
        """
        Searches for films by a keyword in the title.

        Parameters:
            keyword (str): The keyword to search for in film titles.

        Returns:
            List[Tuple]: A list of tuples containing the search results.

        Behavior:
            - Logs the search query.
            - Executes a SELECT query to find films where the title matches the keyword.
        """
        self.log_query(f"keyword: {keyword}")
        query = "SELECT * FROM film WHERE title LIKE %s"
        return self.db_manager.execute_query(query, (f"%{keyword}%",))

    def search_by_genre_and_year(self, genre: str, year: str) -> List[Tuple]:
        """
        Searches for films by genre and release year.

        Parameters:
            genre (str): The genre of the films to search for.
            year (str): The release year of the films to search for.

        Returns:
            List[Tuple]: A list of tuples containing the title, genre, and release year of matching films.

        Behavior:
            - Logs the search query.
            - Executes a SELECT query with joins between the 'film', 'film_category', and 'category' tables
              to find films matching the specified genre and year.
        """
        self.log_query(f"genre: {genre}, year: {year}")
        query = """
            SELECT f.title, c.name, f.release_year
            FROM film f
            JOIN film_category fc ON f.film_id = fc.film_id
            JOIN category c ON fc.category_id = c.category_id
            WHERE c.name = %s AND f.release_year = %s
        """
        return self.db_manager.execute_query(query, (genre, year))

    def search_by_actor(self, actor_name: str) -> List[Tuple]:
        """
        Searches for films by actor name.

        Parameters:
            actor_name (str): The name of the actor to search for.

        Returns:
            List[Tuple]: A list of tuples containing the films where the actor appeared.

        Behavior:
            - Logs the search query.
            - Executes a SELECT query with joins between the 'film', 'film_actor', and 'actor' tables
              to find films where the specified actor appeared.
        """
        self.log_query(f"actor: {actor_name}")
        query = """
            SELECT f.title, CONCAT(a.first_name, ' ', a.last_name) as actor_name
            FROM film f
            JOIN film_actor fa ON f.film_id = fa.film_id
            JOIN actor a ON fa.actor_id = a.actor_id
            WHERE CONCAT(a.first_name, ' ', a.last_name) LIKE %s
        """
        return self.db_manager.execute_query(query, (f"%{actor_name}%",))

    def get_top_queries(self) -> List[Tuple]:
        """
        Retrieves the top 10 most popular search queries.

        Returns:
            List[Tuple]: A list of tuples containing query text and the corresponding count.

        Behavior:
            - Executes a SELECT query on the 'query_logs' table to count the occurrences of each query.
            - Orders the results by count in descending order and limits the output to the top 10.
        """
        query = """
            SELECT query_text, COUNT(*) as count
            FROM query_logs
            GROUP BY query_text
            ORDER BY count DESC
            LIMIT 10
        """
        return self.db_manager.execute_query(query)
