import streamlit as st
from Constants import Constants
from User import User

constants = Constants()
user = User()

# Set page title
st.set_page_config(page_title="Login - Library Management System", layout="centered")

# Login Header
st.markdown("<h2 style='text-align: center;'>Login</h2>", unsafe_allow_html=True)
st.markdown("---")

# Username & Password Input Fields
username = st.text_input("Username", placeholder="Enter your username")
password = st.text_input("Password", type="password", placeholder="Enter your password")

# Login Validation
if st.button("Login"):
    if user.validateSignIn(username, password):
        st.success("Login successful! Redirecting to home page...")

        # Store username in session state for future access
        st.session_state["username"] = username

        st.switch_page(constants.dashboardStudent)
    else:
        st.error("Invalid username or password. Please try again!")

# Sign Up Link
col1, col2 = st.columns([1, 1])

with col2:
    if st.button("📝 Don't have an account? Sign Up"):
        st.switch_page(constants.signup)