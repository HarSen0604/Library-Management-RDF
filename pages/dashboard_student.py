import streamlit as st
from Constants import Constants
from StudentData import StudentData

# Initialize constants and data
constants = Constants()
studentData = StudentData()

# Set page title and layout
st.set_page_config(page_title="Student Dashboard - Library Management System", layout="wide")

# Get logged-in student's username from session state
username = st.session_state.get("username", "Student")

# Top Navigation Bar
col1, col2 = st.columns([1, 2])
with col1:
    st.image(constants.logo, width=100)
with col2:
    # Recommendations Button
    if st.button("📚 Get Recommendations"):
        recommendations = studentData.getRecommendations()
        if recommendations:
            st.markdown("### 🎯 Personalized Recommendations:")
            st.table(recommendations)
        else:
            st.warning("No recommendations available right now!")

# Search Bar
search_option = st.selectbox("Search by", ["Title", "Author", "Genre"])
search_query = st.text_input(f"Search for books by {search_option.lower()}...")

# Display search results with borrow button
# Display search results with borrow button
if search_query:
    search_results = studentData.searchBooks(search_option, search_query)

    if search_results:
        st.markdown("### 🔍 Search Results:")
        for idx, book in enumerate(search_results[:5]):  # Show only first 5 results
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"📘 **{book['title']}** by *{book['author']}* — {book['genre']} ({book['year']})")

            with col2:
                # Check if student already borrowed this book
                if any(b['title'] == book['title'] for b in studentData.getBorrowedBooks(username)):
                    st.button("✅ Already Borrowed", disabled=True, key=f"borrow_disabled_{username}_{book['title']}")
                else:
                    if st.button(f"Borrow {idx+1}", key=f"borrow_{username}_{book['title']}"):
                        print(f"[DEBUG] Attempting to borrow book: {book['title']} for user: {username}")
                        success = studentData.borrowBook(username, book["title"])
                        if success:
                            st.success(f"You have borrowed **{book['title']}** successfully!")
                        else:
                            st.error("Failed to borrow the book. Please try again.")
    else:
        st.warning("No books found matching your search.")

st.markdown("---")

# 📘 Borrowed Books Display with Return Buttons
st.markdown("### 📘 Your Borrowed Books:")

for idx, book in enumerate(studentData.getBorrowedBooks(username)):
    col1, col2 = st.columns([4, 1])
    with col1:
        st.write(f"📕 **{book['title']}** by *{book['author']}* — Due Date: {book['dueDate']}")
    with col2:
        # Return button with unique key for each student-book combo
        if st.button("Return", key=f"return_{username}_{book['title']}"):
            studentData.returnBook(username, book["title"])
            st.success(f"✅ You have returned **{book['title']}** successfully!")
            st.switch_page(constants.dashboardStudent)

st.markdown("---")

# Sign Out Button — clears session and redirects to main page
if st.sidebar.button("🚪 Sign Out"):
    st.session_state.clear()
    st.switch_page(constants.main)

st.sidebar.write("📧 Need Help? [Contact Us](mailto:hod.cse@psgtech.ac.in)")