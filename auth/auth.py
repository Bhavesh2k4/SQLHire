import bcrypt
import streamlit as st
from db.queries import get_database_connection
import pymysql
from pymysql import MySQLError


def init_admin_user():
    """
    Initialize an admin user with default credentials if none exists.
    """
    conn = get_database_connection()
    cursor = None
    if conn:
        try:
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            
            # Check if admin exists
            cursor.execute("SELECT COUNT(*) as count FROM Users WHERE username = 'admin'")
            result = cursor.fetchone()
            admin_exists = result['count'] if result else 0
            
            if not admin_exists:
                # Hash the default password for admin
                default_password = 'admin123'
                hashed_password = bcrypt.hashpw(default_password.encode('utf-8'), bcrypt.gensalt())
                hashed_password_str = hashed_password.decode('utf-8')
                
                # Insert the new admin user
                cursor.execute("""
                    INSERT INTO Users (username, password, role)
                    VALUES (%s, %s, %s)
                """, ('admin', hashed_password_str, 'admin'))
                
                conn.commit()
                st.success("Admin user created successfully!")
            else:
                st.info("Admin user already exists.")
        
        except MySQLError as e:
            st.error(f"Error initializing admin user: {e}")
        
        except Exception as e:
            st.error(f"An unexpected error occurred while initializing admin user: {e}")
        
        finally:
            if cursor:
                cursor.close()
            if conn and conn.open:
                conn.close()
    else:
        st.error("Failed to establish a database connection for initializing admin user.")

def login_user(username, password):
    """
    Authenticates a user by verifying the provided password against the stored hash.
    Returns the user's details (without password) if authentication succeeds, otherwise None.
    """
    conn = get_database_connection()
    cursor = None  # Initialize cursor to None

    if conn:
        try:
            # Create a cursor with dictionary format to fetch data as a dictionary
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            
            # Fetch user by username
            cursor.execute("""
                SELECT user_id, username, password, role 
                FROM Users 
                WHERE username = %s
            """, (username,))
            user = cursor.fetchone()

            # Verify password
            if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                del user['password']  # Remove password from user data before returning
                
                # Store user details in session state for further use
                st.session_state.user_id = user['user_id']
                st.session_state.username = user['username']
                st.session_state.role = user['role']
                
                return user  # Return user details except password
            else:
                st.warning("Invalid username or password.")
            return None
        
        except Exception as e:
            st.error(f"Error logging in: {e}")
        
        finally:
            # Close the cursor and connection only if they were created
            if cursor:
                cursor.close()
            if conn and conn.open:
                conn.close()
    else:
        st.error("Failed to establish a database connection.")
    return None
