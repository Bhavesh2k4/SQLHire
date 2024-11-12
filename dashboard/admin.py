import pymysql.cursors
import streamlit as st
from db.queries import get_database_connection,hash_password
from mysql.connector import Error
import pymysql
from pymysql import MySQLError
import pandas as pd

import streamlit as st

def add_user():
    conn = get_database_connection()
    if conn:
        try:
            cursor = conn.cursor(pymysql.cursors.DictCursor)

            # Capture the role first
            st.subheader("Add User")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            role = st.selectbox("Role", ["student", "company", "admin"])

            # Capture additional details based on the role
            additional_details = {}

            # Dynamic form fields depending on role
            if role == "student":
                st.write("Student Details")
                additional_details['first_name'] = st.text_input("First Name")
                additional_details['last_name'] = st.text_input("Last Name")
                additional_details['email'] = st.text_input("Email")
                additional_details['phone'] = st.text_input("Phone")
                additional_details['cgpa'] = float(st.number_input("CGPA", min_value=0.0, max_value=10.0))
                additional_details['graduation_year'] = st.text_input("Graduation Year")
                additional_details['department'] = st.text_input("Department")
            elif role == "company":
                st.write("Company Details")
                additional_details['company_name'] = st.text_input("Company Name")
                additional_details['industry'] = st.text_input("Industry")
                additional_details['website'] = st.text_input("Website")
                additional_details['description'] = st.text_area("Description")

            submit = st.button("Add User")
            if submit:
                hashed_password = hash_password(password)
                
                # Insert into Users table
                cursor.execute("INSERT INTO Users (username, password, role) VALUES (%s, %s, %s)", 
                               (username, hashed_password, role))
                conn.commit()
                user_id = cursor.lastrowid  # Get the last inserted user_id

                # Insert additional details based on role
                if role == "student":
                    cursor.execute("""
                        INSERT INTO Students (user_id, first_name, last_name, email, phone, cgpa, graduation_year, department)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, (user_id, additional_details['first_name'], additional_details['last_name'],
                          additional_details['email'], additional_details['phone'], 
                          additional_details['cgpa'], additional_details['graduation_year'], 
                          additional_details['department']))
                elif role == "company":
                    cursor.execute("""
                        INSERT INTO Companies (user_id, company_name, industry, website, description)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (user_id, additional_details['company_name'], additional_details['industry'],
                          additional_details['website'], additional_details['description']))

                conn.commit()
                st.success(f"User {username} added successfully!")

        except MySQLError as e:
            st.error(f"Error adding user: {e}")
        finally:
            cursor.close()
            conn.close()


def delete_user():
    conn = get_database_connection()
    if conn:
        try:
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            user_id = st.text_input("User ID to delete", value="", key="delete_user_id")
            if st.button("Delete User"):
                cursor.execute("SELECT role FROM Users WHERE user_id = %s", (user_id,))
                user = cursor.fetchone()
                
                if user:
                    role = user['role']
                    # Delete from Students or Companies based on role
                    if role == 'student':
                        cursor.execute("DELETE FROM Students WHERE user_id = %s", (user_id,))
                    elif role == 'company':
                        cursor.execute("DELETE FROM Companies WHERE user_id = %s", (user_id,))
                    
                    # Then delete from Users table
                    cursor.execute("DELETE FROM Users WHERE user_id = %s", (user_id,))
                    conn.commit()
                    st.success(f"User ID {user_id} deleted successfully!")
                else:
                    st.error("User not found.")
        
        except MySQLError as e:
            st.error(f"Error deleting user: {e}")
        finally:
            cursor.close()
            conn.close()

def view_all_users():
    conn = get_database_connection()
    if conn:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM Users")
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        if users:
            users_df = pd.DataFrame(users)
            st.dataframe(users_df)
        else:
            st.write("No users found.")
    else:
        st.write("Database connection failed.")

def view_statistics():
    conn = get_database_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    

    cursor.execute("""
        SELECT 
            (SELECT COUNT(*) FROM Students) as total_students,
            (SELECT COUNT(*) FROM Companies) as total_companies,
            (SELECT COUNT(*) FROM Jobs) as total_jobs
    """)
    
    stats = cursor.fetchone()  # fetchone since we only expect one row
    st.write(stats)
    
    cursor.close()
    conn.close()


def admin_dashboard():
    st.title("Admin Dashboard")
    action = st.sidebar.selectbox("Choose action", ["Add User", "View All Users", "Delete User", "Statistics"])
    
    if action == "Add User":
        add_user()
    elif action == "View All Users":
        view_all_users()
    elif action == "Delete User":
        delete_user()
    elif action == "Statistics":
        view_statistics()
