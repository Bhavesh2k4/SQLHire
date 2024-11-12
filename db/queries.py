import pymysql
from pymysql import MySQLError
from configdb import DB_CONFIG
import bcrypt

def get_database_connection():
    try:
        print("Attempting to connect to the database...")
        conn = pymysql.connect(**DB_CONFIG)
        if conn.open:
            print("Connection to the database established successfully.")
            return conn
        else:
            print("Connection to the database failed.")
            return None
    except MySQLError as e:
        print(f"Error connecting to database: {e}")
        return None

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

def get_student_email(student_id):
    conn = get_database_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT email FROM Students WHERE student_id = %s", (student_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result["email"] if result else None
