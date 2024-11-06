import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
password=os.getenv('PASSWORD')
username="root"
hostname=os.getenv('HOST')
database=os.getenv('DATABASE')
DB_CONFIG = {
    'host': hostname,
    'user': username,
    'password': password,
    'database': database,
    # 'port' : <port_no> if a specific port is needed 
}
