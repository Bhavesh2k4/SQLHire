import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
password=os.getenv('PASSWORD')
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': password,
    'database': 'placement_db'
}