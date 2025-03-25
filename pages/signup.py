import streamlit as st
from Constants import Constants
from User import User

constants = Constants()
user = User()

# Set page title
st.set_page_config(page_title="Sign Up - Library Management System", layout="centered")

# Sign Up Header
st.markdown("<h2 style='text-align: center;'>Sign Up</h2>", unsafe_allow_html=True)
st.markdown("---")

# Input Fields
username = st.text_input("Username", placeholder="Enter your username")
password = st.text_input("Password", type="password", placeholder="Enter your password")

# Sign Up Button
if st.button("Sign Up"):
    if username and password:
        success, message = user.insertNewUser(username, password)
        if success:
            st.success("Sign up request sent! Awaiting librarian approval.")
            st.switch_page(constants.main)
        else:
            st.error(message)
    else:
        st.error("Please fill in both fields!")

# Back to Home Button
if st.button("🏠 Back to Home"):
    st.switch_page(constants.main)
