import mysql.connector
from mysql.connector import Error
from configdb import DB_CONFIG

DB_INIT_TABLES = """
CREATE TABLE IF NOT EXISTS Users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'student', 'company') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Students (
    student_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15),
    cgpa DECIMAL(4,2),
    graduation_year INT,
    department VARCHAR(50),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE IF NOT EXISTS Companies (
    company_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    company_name VARCHAR(100) NOT NULL,
    industry VARCHAR(50),
    website VARCHAR(100),
    description TEXT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE IF NOT EXISTS Jobs (
    job_id INT PRIMARY KEY AUTO_INCREMENT,
    company_id INT,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    job_type ENUM('internship', 'fulltime') NOT NULL,
    location VARCHAR(100),
    salary_range VARCHAR(50),
    required_cgpa DECIMAL(4,2),
    posting_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deadline TIMESTAMP,
    status ENUM('open', 'closed') DEFAULT 'open',
    FOREIGN KEY (company_id) REFERENCES Companies(company_id)
);

CREATE TABLE IF NOT EXISTS Applications (
    application_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    job_id INT,
    status ENUM('pending', 'shortlisted', 'rejected', 'accepted') DEFAULT 'pending',
    applied_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES Students(student_id),
    FOREIGN KEY (job_id) REFERENCES Jobs(job_id)
);

CREATE TABLE IF NOT EXISTS Student_Skills (
    student_id INT,
    skill_name VARCHAR(50) NOT NULL,
    proficiency_level ENUM('beginner', 'intermediate', 'advanced'),
    PRIMARY KEY (student_id, skill_name),
    FOREIGN KEY (student_id) REFERENCES Students(student_id)
);
"""

def init_database():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            print("Connected to MySQL database.")
        cursor = conn.cursor()
        for statement in DB_INIT_TABLES.split(';'):
            if statement.strip():
                cursor.execute(statement)
        conn.commit()
        print("Database and tables initialized.")
    except Error as e:
        print(f"Error initializing database: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    init_database()
