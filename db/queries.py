import mysql.connector
from configdb import DB_CONFIG
import bcrypt
from mysql.connector import Error

def get_database_connection():
    try:
        print("Attempting to connect to the database ")
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            print("Connection to the database established successfully.")
            return conn
        else:
            print("Connection to the database failed.")
            return None
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

def get_student_email(student_id):
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM Students WHERE student_id = %s", (student_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None
