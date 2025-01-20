class ConsoleInterface:
    """
    Manages the console-based user interface for the film search system.
    """

    def __init__(self, searcher):
        self.searcher = searcher

    def display_results(self, results):
        """
        Displays search results in the console.
        """
        if results:
            for row in results:
                print(row)
        else:
            print("Nothing found.")

    def run(self):
        """
        Runs the main interactive console loop for the film search system.
        """
        print("Welcome to the Film Search System!")
        while True:
            print("\nAvailable commands:")
            print("1. Search by keyword")
            print("2. Search by genre and year")
            print("3. Search by actor")
            print("4. Top popular queries")
            print("5. Exit")
            choice = input("Enter the command number: ")

            try:
                if choice == "1":
                    keyword = input("Enter a keyword to search: ")
                    results = self.searcher.search_by_keyword(keyword)
                    self.display_results(results)
                elif choice == "2":
                    genre = input("Enter the genre: ")
                    year = input("Enter the year: ")
                    results = self.searcher.search_by_genre_and_year(genre, year)
                    self.display_results(results)
                elif choice == "3":
                    actor_name = input("Enter the actor's name: ")
                    results = self.searcher.search_by_actor(actor_name)
                    self.display_results(results)
                elif choice == "4":
                    print("Top 10 popular queries:")
                    results = self.searcher.get_top_queries()
                    self.display_results(results)
                elif choice == "5":
                    print("Exiting the program. Goodbye!")
                    break
                else:
                    print("Invalid input. Please try again.")
            except Exception as e:
                print(f"An error occurred: {e}")
