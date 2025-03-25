from SPARQLWrapper import SPARQLWrapper, JSON, POST
import requests

FUSEKI_QUERY_URL = "http://localhost:3030/libraryDS/query"
FUSEKI_UPDATE_URL = "http://localhost:3030/libraryDS/update"

class User:
    def __init__(self):
        self.sparql = SPARQLWrapper(FUSEKI_QUERY_URL)

    def validateSignIn(self, username, password):
        """ Validates login credentials """
        query = f"""
        PREFIX lib: <http://www.semanticweb.org/santhoshir/ontologies/2025/2/library/>
        ASK {{
            ?user lib:username "{username}" ;
                  lib:password "{password}" .
        }}
        """
        self.sparql.setQuery(query)
        self.sparql.setReturnFormat(JSON)
        return self.sparql.query().convert().get("boolean", False)

    def insertNewUser(self, username, password):
        """ Registers a new user as pending approval """
        update_query = f"""
        PREFIX lib: <http://www.semanticweb.org/santhoshir/ontologies/2025/2/library/>
        INSERT DATA {{
            lib:User_{username.replace(" ", "_")} a lib:Student ;
                lib:username "{username}" ;
                lib:password "{password}" ;
                lib:email "{username}@example.com" ;
                lib:registrationDate "2025-03-20" ;
                lib:pendingApproval "true" .
        }}
        """
        return self.execute_update(update_query), "User registration request submitted."

    def getPendingUsers(self):
        """ Retrieves all pending users """
        query = """
        PREFIX lib: <http://www.semanticweb.org/santhoshir/ontologies/2025/2/library/>
        SELECT ?username WHERE {
            ?user a lib:Student ;
                  lib:username ?username ;
                  lib:pendingApproval "true" .
        }
        """
        return self.execute_query(query)

    def approveUser(self, username):
        """ Approves a user by removing pending status """
        update_query = f"""
        PREFIX lib: <http://www.semanticweb.org/santhoshir/ontologies/2025/2/library/>
        DELETE {{
            ?user lib:pendingApproval "true" .
        }}
        INSERT {{
            ?user lib:approved "true" .
        }}
        WHERE {{
            ?user a lib:Student ;
                  lib:username "{username}" .
        }}
        """
        return self.execute_update(update_query)

    def rejectUser(self, username):
        """ Removes a pending user from the database """
        update_query = f"""
        PREFIX lib: <http://www.semanticweb.org/santhoshir/ontologies/2025/2/library/>
        DELETE WHERE {{
            ?user a lib:Student ;
                  lib:username "{username}" .
        }}
        """
        return self.execute_update(update_query)

    def execute_query(self, query):
        self.sparql.setQuery(query)
        self.sparql.setReturnFormat(JSON)
        results = self.sparql.query().convert()
        return [result["username"]["value"] for result in results.get("results", {}).get("bindings", [])]

    def execute_update(self, update_query):
        response = requests.post(FUSEKI_UPDATE_URL, data={"update": update_query})
        return response.status_code == 200