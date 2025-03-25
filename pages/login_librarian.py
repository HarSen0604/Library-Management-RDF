import streamlit as st
from Constants import Constants
from User import User

constants = Constants()
user = User()

# Set page title
st.set_page_config(page_title="Librarian Login - Library Management System", layout="centered")

# Login Header
st.markdown("<h2 style='text-align: center;'>Librarian Login</h2>", unsafe_allow_html=True)
st.markdown("---")

# Username & Password Input Fields
username = st.text_input("Username", placeholder="Enter your librarian username")
password = st.text_input("Password", type="password", placeholder="Enter your password")

# Login Validation
if st.button("Login"):
    # Hardcode librarian credentials for now
    if username == "admin" and password == "librarian":
        st.success("Librarian login successful! Redirecting to dashboard...")

        # Store librarian session
        st.session_state["librarian"] = username

        st.switch_page(constants.dashboardLibrarian)
    else:
        st.error("Invalid librarian credentials. Please try again!")

# Back to Home Button
if st.button("🏠 Back to Home"):
    st.switch_page(constants.main)
