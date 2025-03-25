from SPARQLWrapper import SPARQLWrapper, JSON, POST
import requests

FUSEKI_QUERY_URL = "http://localhost:3030/libraryDS/query"
FUSEKI_UPDATE_URL = "http://localhost:3030/libraryDS/update"

class BookManager:
    def __init__(self):
        self.sparql = SPARQLWrapper(FUSEKI_QUERY_URL)

    def get_all_books(self):
        """ Retrieves all books with unique entries """
        query = """
        PREFIX lib: <http://www.semanticweb.org/santhoshir/ontologies/2025/2/library/>
        SELECT DISTINCT ?book ?title ?author ?genre ?year ?availableCopies
        WHERE {
            ?book a lib:Book ;
                  lib:title ?title ;
                  lib:writtenBy ?author ;
                  lib:hasGenre ?genre ;
                  lib:publicationDate ?year ;
                  lib:availableCopies ?availableCopies .
        }
        """
        books = self.execute_query(query, ["title", "author", "genre", "year", "availableCopies"])
        
        # Ensure the field names match the expected format in Streamlit UI
        for book in books:
            book["Available"] = book.pop("Availablecopies", "0")  # Fix key mismatch
        
        return books

    def add_book(self, title, author, genre, year, available):
        print(f"Adding book: {title} by {author} ({year})")  # Debugging statement

        # Check if a book with the same title, author, year, and genre already exists
        query = f"""
        PREFIX lib: <http://www.semanticweb.org/santhoshir/ontologies/2025/2/library/>
        ASK {{
            ?book a lib:Book ;
                lib:title "{title}" ;
                lib:writtenBy "{author}" ;
                lib:hasGenre "{genre}" ;
                lib:publicationDate "{year}" .
        }}
        """

        self.sparql.setQuery(query)
        self.sparql.setReturnFormat(JSON)
        if self.sparql.query().convert().get("boolean", False):
            print(f"Book '{title}' by '{author}' ({year}, {genre}) already exists. Skipping insertion.")
            return False  # Book already exists

        # Generate a unique URI based on title, author, year
        uri_safe_title = title.replace(" ", "_").replace('"', '')
        uri_safe_author = author.replace(" ", "_").replace('"', '')
        book_uri = f"lib:Book_{uri_safe_title}_{uri_safe_author}_{year}"

        update_query = f"""
        PREFIX lib: <http://www.semanticweb.org/santhoshir/ontologies/2025/2/library/>
        INSERT DATA {{
            {book_uri} a lib:Book ;
                lib:title "{title}" ;
                lib:writtenBy "{author}" ;
                lib:hasGenre "{genre}" ;
                lib:publicationDate "{year}" ;
                lib:availableCopies "{available}" .
        }}
        """
        return self.execute_update(update_query)

    def edit_book(self, old_title, new_title=None, new_author=None, new_genre=None, new_year=None, new_available=None):
        """ Updates an existing book entry while preserving unchanged fields """
        query = f"""
        PREFIX lib: <http://www.semanticweb.org/santhoshir/ontologies/2025/2/library/>
        SELECT ?book ?title ?author ?genre ?year ?availableCopies
        WHERE {{
            ?book a lib:Book ;
                lib:title "{old_title}" ;
                lib:writtenBy ?author ;
                lib:hasGenre ?genre ;
                lib:publicationDate ?year ;
                lib:availableCopies ?availableCopies .
        }}
        """
        
        existing_books = self.execute_query(query, ["book", "title", "author", "genre", "year", "availableCopies"])
        if not existing_books:
            print(f"Book '{old_title}' not found.")
            return False
        
        book_uri = existing_books[0]["Book"]  # Retrieve book identifier
        old_data = existing_books[0]
        
        update_query = f'''PREFIX lib: <http://www.semanticweb.org/santhoshir/ontologies/2025/2/library/>
        DELETE WHERE {{
            <{book_uri}> lib:title "{old_title}" ;
                        lib:writtenBy ?author ;
                        lib:hasGenre ?genre ;
                        lib:publicationDate ?year ;
                        lib:availableCopies ?availableCopies .
        }};
        INSERT DATA {{
            <{book_uri}> lib:title "{new_title or old_data['Title']}" ;
                        lib:writtenBy "{new_author or old_data['Author']}" ;
                        lib:hasGenre "{new_genre or old_data['Genre']}" ;
                        lib:publicationDate "{new_year or old_data['Year']}" ;
                        lib:availableCopies "{new_available or old_data['Available']}" .
        }}'''
        return self.execute_update(update_query)

    def delete_book(self, title, author, genre, year):
        """ Deletes the book with matching title, author, genre, and year """
        # Step 1: Fetch the URI of the exact book
        query = f"""
        PREFIX lib: <http://www.semanticweb.org/santhoshir/ontologies/2025/2/library/>
        SELECT ?book WHERE {{
            ?book a lib:Book ;
                lib:title "{title}" ;
                lib:writtenBy "{author}" ;
                lib:hasGenre "{genre}" ;
                lib:publicationDate "{year}" .
        }}
        """
        result = self.execute_query(query, ["book"])
        if not result:
            print(f"❌ No exact match found for: {title}, {author}, {genre}, {year}")
            return False

        book_uri = result[0]["Book"]

        # Step 2: Delete all triples for the specific book
        update_query = f"""
        DELETE WHERE {{
            <{book_uri}> ?p ?o .
        }}
        """
        return self.execute_update(update_query)

    def execute_query(self, query, fields):
        self.sparql.setQuery(query)
        self.sparql.setReturnFormat(JSON)
        try:
            results = self.sparql.query().convert()
            return [
                {field.capitalize(): res.get(field, {}).get("value", "Unknown") for field in fields}
                for res in results.get("results", {}).get("bindings", [])
            ]
        except Exception as e:
            print(f"SPARQL Query Error: {e}")
            return []

    def execute_update(self, update_query):
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        try:
            response = requests.post(FUSEKI_UPDATE_URL, data={"update": update_query}, headers=headers)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"SPARQL Update Error: {e}")
            return False
