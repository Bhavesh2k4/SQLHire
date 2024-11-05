# SQLHire
SQLHire is a simple DBMS + web-based application built with MySQL and Python-Streamlit, designed as a replica of a placement and internship platform.(Built as a Mini-Project for my semester 5 DBMS course)

```plaintext
placement-management-system/
|-- auth/
|   |-- auth.py                  # Authentication and user management
|-- dashboard/
|   |-- admin.py                 # Admin dashboard functionality
|   |-- company.py               # Company dashboard functionality
|   |-- student.py               # Student dashboard functionality
|-- db/
|   |-- init_db.py              # Database initialization
|   |-- proc_trig.py            # Stored procedures and triggers
|   |-- queries.py              # Database queries
|-- notifications/
|   |-- email.py                # Email notification system
|-- .env                        # Environment variables
|-- .gitignore                  # Git ignore file
|-- app.py                      # Main application entry point
|-- configdb.py                 # Database configuration
```

## Setup Instructions
1. **Technologies Used**
     ```
     Python 3.x
     MySQL
     Streamlit
     Bcrypt
     dotenv
     Python MySQL Connector
     
     ```
2. **Requirements**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Variables**
   - Create a `.env` file in the root directory with the following environment variables:
     ```env
     EMAIL=<your_email_address> #(This is the From Email Address in your Application)
     EMAIL_PASSWORD=<your_email_password> #(Setup App Password in Google)
     PASSWORD=<your_database_password>
     HOST=<your_database_host> #ex localhost if you are running it locally
     USER=<your_database_user> #ex root
     DATABASE=<your_database_password> #ex placement_db
     ```

4. **Run the Application**
   - Start the Streamlit app:
     ```bash
     streamlit run app.py
     ```

## Features

1. **Multi-User Authentication System**
   - Student, Company, and Admin roles
   - Secure password hashing
   - Session management

2. **Student Features**
   - Profile management
   - Skills management
   - Job applications
   - Application status tracking

3. **Company Features**
   - Company profile management
   - Job posting
   - Application management
   - Candidate shortlisting

4. **Admin Features**
   - User management
   - System statistics

5. **Notifications**
   - `notifications/email.py`: Sends emails to students notifying them of their application status updates.

## Database Schema
**Relational Schema**
![image](https://github.com/user-attachments/assets/f4581164-aa84-4898-a3e1-d96ade1f3b2d)

**ER Diagram**
![image](https://github.com/user-attachments/assets/00b7a852-d966-4a11-bcb9-63ce2b47abb3)

## Licence
This project is licensed under the MIT License.

