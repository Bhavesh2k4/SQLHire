import bcrypt
import streamlit as st
from db.queries import get_database_connection

def init_admin_user():
    """
    Initialize an admin user with default credentials if none exists.
    """
    conn = get_database_connection()
    if conn:
        try:
            cursor = conn.cursor()
            
            # Check if admin exists
            cursor.execute("SELECT COUNT(*) FROM Users WHERE username = 'admin'")
            admin_exists = cursor.fetchone()[0]
            
            if not admin_exists:
                # Create admin with hashed password
                hashed_password = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt())
                
                cursor.execute("""
                    INSERT INTO Users (username, password, role)
                    VALUES (%s, %s, %s)
                """, ('admin', hashed_password.decode('utf-8'), 'admin'))
                
                conn.commit()
                st.success("Admin user created successfully!")
        except Exception as e:
            st.error(f"Error creating admin user: {e}")
        finally:
            cursor.close()
            conn.close()

def login_user(username, password):
    """
    Authenticates a user by verifying the provided password against the stored hash.
    Returns the user's details (without password) if authentication succeeds, otherwise None.
    """
    conn = get_database_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
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
            return None
        except Exception as e:
            st.error(f"Error logging in: {e}")
        finally:
            cursor.close()
            conn.close()
    return None