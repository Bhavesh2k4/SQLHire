import os
from dotenv import load_dotenv
import pymysql

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables

password = os.getenv('PASSWORD')
database = os.getenv('DATABASE')
port = int(os.getenv('PORT', 3306))  # Default to 3306 if PORT is not specified

# Database configuration
DB_CONFIG = {
    'host': "mysql-sqlhire-sqlhire.d.aivencloud.com",
    'user': "avnadmin",
    'password': password,
    'database': database,
    'port': port,
    'charset': "utf8mb4",
    'connect_timeout': 10,
    'read_timeout': 10,
    'write_timeout': 10,
    'cursorclass': pymysql.cursors.DictCursor
}
