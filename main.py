from Constants import Constants
import streamlit as st

constants = Constants()

# Set page title
st.set_page_config(page_title="Library Management System", layout="wide")

# Top navigation bar
col1, col2, col3 = st.columns([3, 1, 1])

with col1:
    st.image(constants.logo, width=100)

with col2:
    if st.button("Student Login"):
        st.switch_page(constants.loginStudent)

# Librarian Login Button
with col3:
    if st.button("Librarian Login"):
        st.switch_page(constants.loginLibrarian)

# Main Content
st.markdown("<h1 style='text-align: center;'>Welcome to Library Management System</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>\"Discover a smarter, semantic way to manage books\"</h3>", unsafe_allow_html=True)

# Footer
st.markdown("---")
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("ℹ️ [About](https://www.psgtech.edu)", unsafe_allow_html=True)

with col2:
    st.markdown("📧 [Contact](mailto:hod.cse@psgtech.ac.in)", unsafe_allow_html=True)
