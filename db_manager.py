import pymysql
from typing import List, Tuple
import os

class DatabaseManager:
    """
    A class to manage the connection to a MySQL database and provide methods
    for executing queries and managing the connection lifecycle.
    """

    def __init__(self):
        """
        Initializes the DatabaseManager by loading environment variables and establishing
        a connection to the MySQL database.
        """

        try:
            # Establish a connection to the MySQL database using credentials from environment variables
            self.connection = pymysql.connect(
                host=os.getenv("DB_HOST"),  # Database host address
                user=os.getenv("DB_USER"),  # Database username
                password=os.getenv("DB_PASSWORD"),  # Database password
                database=os.getenv("DB_NAME"),  # Name of the database
                port=int(os.getenv("DB_PORT")),  # Port number (default MySQL port is 3306)
                autocommit=False,  # Disable autocommit to manage transactions manually
            )
            self.cursor = self.connection.cursor()  # Create a cursor for executing queries
        except pymysql.MySQLError as e:
            raise RuntimeError(f"Failed to connect to the database: {e}")

    def execute_query(self, query: str, params: Tuple = ()) -> List[Tuple]:
        """
        Executes a SQL query and retrieves the results.

        Parameters:
            query (str): The SQL query to execute.
            params (Tuple): Optional parameters to include in the query (default is an empty tuple).

        Returns:
            List[Tuple]: A list of tuples containing the query results, or an empty list if an error occurs.
        """
        try:
            # Execute the query with the provided parameters
            self.cursor.execute(query, params)
            if query.strip().lower().startswith("select"):
                # Fetch and return all rows if it is a SELECT query
                return self.cursor.fetchall()
            else:
                # Commit changes for non-SELECT queries (e.g., INSERT, UPDATE, DELETE)
                self.connection.commit()
                return []
        except pymysql.MySQLError as e:
            # Rollback changes if an error occurs during query execution
            self.connection.rollback()
            raise RuntimeError(f"Error executing query: {e}")

    def close(self):
        """
        Closes the connection to the MySQL database.

        Ensures that the connection is properly closed when the DatabaseManager instance is no longer in use.
        """
        if self.connection:
            try:
                self.connection.close()  # Close the database connection
            except pymysql.MySQLError as e:
                raise RuntimeError(f"Error closing the database connection: {e}")
