# Semantic Web-Based Library Management System

## About the Project

This project is a **Semantic Web-based Library Management System** that aims to enhance traditional library software using technologies such as **RDF**, **OWL**, and **SPARQL**. Unlike conventional systems that rely on relational databases, this system adopts ontology-driven data modeling to support **semantic-based search**, **automated reasoning**, and **personalized book recommendations**.

By leveraging the power of the Semantic Web, this system allows:

- Structured and machine-readable metadata representation
- Conceptual queries using SPARQL
- Inference-based logic for borrowing rules and recommendations
- Easy integration with external linked data sources
- Role-based access for librarians and students
- Web-based interface for intuitive interaction

## Features

- RDF-based metadata for library books and users
- OWL ontology to define semantic relationships
- SPARQL-powered advanced querying
- Inference engine to detect overdue borrowings
- Ontology-driven book recommendations
- Role-based access control (Student, Librarian)
- Web interface built using Streamlit
- Fuseki backend server for triple-store data access

---

## Getting Started

### Pre-requisites

Make sure the following tools are installed and configured on your system:

1. **Apache Jena Fuseki**  
   - Download: https://jena.apache.org/documentation/fuseki2/#download-fuseki  
   - After installation, **add Fuseki to your system PATH** (via Environmental Variables on Windows or `.bashrc/.zshrc` on POSIX systems)

2. **Protégé**  
   - Download: https://protege.stanford.edu/software.php#desktop-protege  
   - Follow the installation instructions and ensure Protégé is accessible from the terminal or command prompt.

3. **Python 3.x**  
   - Download: https://www.python.org/downloads/  
   - Ensure you check **"Add Python 3.x to PATH"** during installation.

4. **Visual Studio Code** or any code editor of your choice.

---

### Deployment Steps

1. **Import Ontology into Protégé**  
   Open Protégé and import the `lib_ont.ttl` file (available in the repo) into **Active Ontologies**.

2. **Clone the Repository**  
   ```bash
   git clone https://github.com/SanthoshiRavi/Library-Management-RDF.git
   cd Library-Management-RDF
   ```

3. **Install Dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Start Apache Jena Fuseki Server**  
   ```bash
   fuseki-server
   ```

5. **Import RDF Instances into Apache Jena**
 
   Open http://localhost:3030/ on any browser. Then go to 'manage' -> 'Add New Database' and add the .ttl files from the directory 'FinalData' (available in the repo)  

6. **Run the Application using Streamlit**  
   ```bash
   streamlit run main.py
   ```

---

## License

This project is open-source and available under the [MIT License](LICENSE).

---

## References

- [RDF 1.1 Primer – W3C](https://www.w3.org/TR/rdf11-primer/)
- [OWL 2 Web Ontology Language Primer – W3C](https://www.w3.org/TR/owl2-primer/)
- [SPARQL 1.1 Overview – W3C](https://www.w3.org/TR/sparql11-overview/)
- [Apache Jena Fuseki Documentation](https://jena.apache.org/documentation/fuseki2/)
