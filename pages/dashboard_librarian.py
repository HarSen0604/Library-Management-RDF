import streamlit as st
from Constants import Constants
from User import User
from BookManager import BookManager

# Initialize classes
constants = Constants()
user = User()
book_manager = BookManager()

# Ensure only librarian can access this page
if "librarian" not in st.session_state:
    st.error("Unauthorized access!")
    st.stop()

# Set page title
st.set_page_config(page_title="Librarian Dashboard", layout="wide")

# Header
st.markdown("<h2 style='text-align: center;'>📚 Librarian Dashboard</h2>", unsafe_allow_html=True)
st.markdown("---")
st.sidebar.title("📌 Navigation")
st.sidebar.page_link(constants.dashboardLibrarian, label="🏠 Dashboard", icon="🏠")
st.sidebar.page_link(constants.main, label="🔓 Logout", icon="🚪")

# Welcome message
st.markdown(f"### 👋 Welcome, Librarian!")

# Manage Users Section
st.markdown("## 🛠️ Manage Pending User Signups")
pending_users = user.getPendingUsers()

if pending_users:
    for pending_user in pending_users:
        col1, col2 = st.columns([3, 1])
        col1.write(f"📌 **Username:** {pending_user}")
        if col2.button("✅ Approve", key=f"approve_{pending_user}"):
            user.approveUser(pending_user)
        if col2.button("❌ Reject", key=f"reject_{pending_user}"):
            user.rejectUser(pending_user)
        st.switch_page(constants.dashboardLibrarian)
else:
    st.info("No pending user signups.")

# --- Book Management Section ---
st.markdown("---")
st.markdown("## 📚 Manage Books")

# Display current books
st.markdown("### 📖 Current Book List")
books = book_manager.get_all_books()
for book in books:
    st.write(f"📚 **{book['Title']}** by *{book['Author']}* ({book['Year']}), Genre: {book['Genre']}, Available: {book['Available']}")

# --- Add a New Book ---
st.markdown("---")
st.markdown("### ➕ Add a New Book")
with st.form("add_book_form"):
    new_title = st.text_input("Title")
    new_author = st.text_input("Author")
    new_genre = st.text_input("Genre")
    new_year = st.number_input("Year", min_value=1900, max_value=2025, step=1)
    new_available = st.number_input("Available Copies", min_value=1, step=1)
    submitted = st.form_submit_button("Add Book")

    if submitted:
        book_manager.add_book(new_title, new_author, new_genre, new_year, new_available)
        st.success("✅ Book added successfully!")
        st.switch_page(constants.dashboardLibrarian)

# --- Edit an Existing Book ---
st.markdown("---")
st.markdown("### ✏️ Edit an Existing Book")
with st.form("edit_book_form"):
    old_title = st.selectbox("Select a book to edit", [book['Title'] for book in books])
    updated_title = st.text_input("New Title", old_title)
    updated_author = st.text_input("New Author")
    updated_genre = st.text_input("New Genre")
    updated_year = st.number_input("New Year", min_value=1000, max_value=2025, step=1)
    updated_available = st.number_input("New Available Copies", min_value=0, step=1)
    edit_submitted = st.form_submit_button("Edit Book")

    if edit_submitted:
        if book_manager.edit_book(old_title, updated_title, updated_author, updated_genre, updated_year, updated_available):
            st.success("✅ Book details updated!")
            st.switch_page(constants.dashboardLibrarian)
        else:
            st.error("⚠️ Book not found!")

# --- Delete a Book ---
st.markdown("---")
st.markdown("### 🗑️ Delete a Book")

# Build user-friendly dropdown entries with full details
book_options = [
    f"{book['Title']} | {book['Author']} | {book['Genre']} | {book['Year']} | Available: {book['Available']}"
    for book in books
]

# Map display string back to original book details
book_map = {entry: book for entry, book in zip(book_options, books)}

with st.form("delete_book_form"):
    selected_entry = st.selectbox("Select a book to delete", book_options)
    delete_submitted = st.form_submit_button("Delete Book")

    if delete_submitted:
        selected_book = book_map[selected_entry]
        book_manager.delete_book(
            title=selected_book["Title"],
            author=selected_book["Author"],
            genre=selected_book["Genre"],
            year=selected_book["Year"]
        )
        st.success("✅ Book deleted successfully!")
        st.switch_page(constants.dashboardLibrarian)

# --- Dashboard Overview Placeholder ---
st.markdown("---")
st.markdown("## 📊 Dashboard Overview")
st.markdown("- Overdue Books: **5**")
st.markdown("- Recent Activity: **3 new transactions**")

# Footer
st.markdown("---")
st.markdown("ℹ️ [About](https://www.psgtech.edu) | 📧 [Contact](mailto:hod.cse@psgtech.ac.in)")
