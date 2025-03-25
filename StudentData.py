from SPARQLWrapper import SPARQLWrapper, JSON
from datetime import datetime, timedelta
import requests

FUSEKI_QUERY_URL = "http://localhost:3030/libraryDS/query"
FUSEKI_UPDATE_URL = "http://localhost:3030/libraryDS/update"

class StudentData:
    def __init__(self):
        self.sparql = SPARQLWrapper(FUSEKI_QUERY_URL)

    def getBorrowedBooks(self, username):
        """ Fetches books borrowed by a student """
        query = f"""
        PREFIX lib: <http://www.semanticweb.org/santhoshir/ontologies/2025/2/library/>
        SELECT DISTINCT ?title ?author ?borrowDate ?dueDate
        WHERE {{
            ?record a lib:BorrowRecord ;
                    lib:borrowedBy "{str(username)}" ;
                    lib:borrowedBook ?book ;
                    lib:borrowDate ?borrowDate ;
                    lib:dueDate ?dueDate .
            ?book lib:title ?title ;
                  lib:writtenBy ?author .
        }}
        """
        return self.execute_query(query, ["title", "author", "borrowDate", "dueDate"])

    def borrowBook(self, username, book_title):
        """ Allows a student to borrow a book if available """

        print(f"[DEBUG] Attempting to borrow book: {book_title} for user: {username}")

        # Query to fetch the book URI and available copies
        query = f"""
        PREFIX lib: <http://www.semanticweb.org/santhoshir/ontologies/2025/2/library/>
        SELECT ?book ?availableCopies
        WHERE {{
            ?book a lib:Book ;
                lib:title ?storedTitle ;
                lib:availableCopies ?availableCopies .
            FILTER (STR(?storedTitle) = "{book_title}")
        }}
        """
        print("[DEBUG] Running Query in Python:")
        print(query)

        books = self.execute_query(query, ["book", "availableCopies"])

        if not books:
            print(f"[ERROR] No matching book found for title: {book_title}")
            return False  # Book not found

        book_uri = books[0].get("book", "").strip()  # Ensure no extra spaces
        available_copies = books[0].get("availableCopies", "1").strip()  # Default to 1 if missing

        if not book_uri:
            print("[ERROR] Book URI is None or empty. Borrowing cannot proceed.")
            return False

        try:
            available_copies = int(available_copies.replace('"', ''))  # Convert string to integer safely
        except ValueError:
            print(f"[ERROR] Invalid availableCopies value: {available_copies}")
            return False

        print(f"[DEBUG] Retrieved Book URI: {book_uri}, Available Copies: {available_copies}")

        if available_copies <= 0:
            print(f"[DEBUG] Book {book_title} is out of stock")
            return False  # Book not available

        borrow_date = datetime.today().strftime("%Y-%m-%d")
        due_date = (datetime.today() + timedelta(days=14)).strftime("%Y-%m-%d")

        update_query = f"""
        PREFIX lib: <http://www.semanticweb.org/santhoshir/ontologies/2025/2/library/>
        INSERT DATA {{
            lib:BorrowRecord_{username}_{book_title.replace(" ", "_")} a lib:BorrowRecord ;
                lib:borrowedBy "{username}" ;
                lib:borrowedBook <{book_uri}> ;
                lib:borrowDate "{borrow_date}" ;
                lib:dueDate "{due_date}" .
        }};
        DELETE {{ <{book_uri}> lib:availableCopies ?count }}
        INSERT {{ <{book_uri}> lib:availableCopies "{available_copies - 1}" }}
        WHERE {{ <{book_uri}> lib:availableCopies ?count }}
        """
        
        print(f"[DEBUG] Executing SPARQL Update:\n{update_query}")
        return self.execute_update(update_query)

    def returnBook(self, username, book_title):
        """ Allows a student to return a borrowed book """

        print(f"[DEBUG] Attempting to return book: {book_title} for user: {username}")

        # Query to fetch the book URI and borrow record
        query = f"""
        PREFIX lib: <http://www.semanticweb.org/santhoshir/ontologies/2025/2/library/>
        SELECT ?book ?availableCopies ?record
        WHERE {{
            ?record a lib:BorrowRecord ;
                    lib:borrowedBy "{username}" ;
                    lib:borrowedBook ?book ;
                    lib:borrowDate ?borrowDate ;
                    lib:dueDate ?dueDate .
            ?book lib:title "{book_title}" ;
                  lib:availableCopies ?availableCopies .
        }}
        """
        print("[DEBUG] Running Query in Python:")
        print(query)

        results = self.execute_query(query, ["book", "availableCopies", "record"])

        if not results:
            print(f"[ERROR] No matching borrow record found for title: {book_title}")
            return False  # Borrow record not found

        book_uri = results[0].get("book", "").strip()  # Ensure no extra spaces
        available_copies = results[0].get("availableCopies", "1").strip()  # Default to 1 if missing
        record_uri = results[0].get("record", "").strip()  # Borrow record URI

        if not book_uri or not record_uri:
            print("[ERROR] Book URI or Record URI is None or empty. Returning cannot proceed.")
            return False

        try:
            available_copies = int(available_copies.replace('"', ''))  # Convert string to integer safely
        except ValueError:
            print(f"[ERROR] Invalid availableCopies value: {available_copies}")
            return False

        print(f"[DEBUG] Retrieved Book URI: {book_uri}, Available Copies: {available_copies}, Record URI: {record_uri}")

        # Update query to delete the borrow record and increment available copies
        update_query = f"""
        PREFIX lib: <http://www.semanticweb.org/santhoshir/ontologies/2025/2/library/>
        DELETE {{ <{record_uri}> ?p ?o }}
        WHERE {{ <{record_uri}> ?p ?o }};
        DELETE {{ <{book_uri}> lib:availableCopies ?count }}
        INSERT {{ <{book_uri}> lib:availableCopies "{available_copies + 1}" }}
        WHERE {{ <{book_uri}> lib:availableCopies ?count }}
        """
        
        print(f"[DEBUG] Executing SPARQL Update:\n{update_query}")
        return self.execute_update(update_query)

    def searchBooks(self, search_option, query_text):
        """ Searches books based on title, author, or genre """
        field_map = {
            "Title": "?title",
            "Author": "?author",
            "Genre": "?genre"
        }
        field = field_map.get(search_option, "?title")
        
        query = f"""
        PREFIX lib: <http://www.semanticweb.org/santhoshir/ontologies/2025/2/library/>
        SELECT DISTINCT ?title ?author ?genre ?year
        WHERE {{
            ?book a lib:Book ;
                  lib:title ?title ;
                  lib:writtenBy ?author ;
                  lib:hasGenre ?genre ;
                  lib:publicationDate ?year .
            FILTER regex({field}, "{query_text}", "i") 
        }}
        """
        print(f"[DEBUG] Executing SPARQL Query:\n{query}")
        return self.execute_query(query, ["title", "author", "genre", "year"])

    def getRecommendations(self):
        """ Fetches book recommendations based on borrowing history """
        query = """
        PREFIX lib: <http://www.semanticweb.org/santhoshir/ontologies/2025/2/library/>
        SELECT DISTINCT ?title ?author ?genre ?year
        WHERE {
            ?book a lib:Book ;
                  lib:title ?title ;
                  lib:writtenBy ?author ;
                  lib:hasGenre ?genre ;
                  lib:publicationDate ?year .
        }
        ORDER BY RAND()
        LIMIT 5
        """
        return self.execute_query(query, ["title", "author", "genre", "year"])

    def execute_query(self, query, fields):
        """ Executes a SPARQL SELECT query and returns results with correctly formatted keys """
        self.sparql.setQuery(query)
        self.sparql.setReturnFormat(JSON)

        try:
            results = self.sparql.query().convert()
            print("[DEBUG] Raw SPARQL Query Results:")
            print(results)  # Print raw results for debugging

            books = []
            for result in results["results"]["bindings"]:
                book = {}
                for field in fields:
                    if field in result:
                        book[field] = result[field]["value"]  # Use the original field name (lowercase)
                    else:
                        book[field] = "Unknown"
                books.append(book)
            return books
        except Exception as e:
            print(f"[ERROR] SPARQL Query Error: {e}")
            print(f"[DEBUG] Failed Query:\n{query}")
            return []

    def execute_update(self, update_query):
        """ Executes a SPARQL UPDATE query """
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        try:
            response = requests.post(FUSEKI_UPDATE_URL, data={"update": update_query}, headers=headers)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] SPARQL Update Error: {e}")
            print(f"[DEBUG] Failed Query:\n{update_query}")
            return False