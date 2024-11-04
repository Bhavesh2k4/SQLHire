import streamlit as st
from auth.auth import init_admin_user, login_user
from dashboard.student import student_dashboard
from dashboard.company import company_dashboard
from dashboard.admin import admin_dashboard
from db.init_db import init_database
from db.proc_trig import create_triggers_and_procedures

# Initialize the app
st.set_page_config(page_title="Placement Management System")
init_database()
create_triggers_and_procedures()
# Initialize admin user on first run
init_admin_user()

# Define session state for user authentication
if 'user' not in st.session_state:
    st.session_state.user = None

# Login form for user authentication
def show_login():
    st.title("Login to Placement Management System")
    
    # Collect username and password inputs
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = login_user(username, password)
        if user:
            st.session_state.user = user
            st.success(f"Welcome, {user['username']}!")
        else:
            st.error("Invalid username or password")

# Logout function
def logout():
    st.session_state.user = None
    st.info("You have successfully logged out.")

# Render user dashboard based on role
def render_dashboard():
    user = st.session_state.user
    if user['role'] == 'admin':
        admin_dashboard()
    elif user['role'] == 'company':
        company_dashboard()
    elif user['role'] == 'student':
        student_dashboard()
    else:
        st.error("Unauthorized access")

# Main app logic
if st.session_state.user is None:
    show_login()
else:
    st.sidebar.title(f"Welcome, {st.session_state.user['username']} ({st.session_state.user['role']})")
    if st.sidebar.button("Logout"):
        logout()
    else:
        render_dashboard()
