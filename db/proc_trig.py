import mysql.connector
from configdb import DB_CONFIG

TRIGGER_SCRIPT = """
CREATE TRIGGER before_application_insert
BEFORE INSERT ON Applications
FOR EACH ROW
BEGIN
    DECLARE student_cgpa DECIMAL(4,2);
    DECLARE job_min_cgpa DECIMAL(4,2);
    
    SELECT cgpa INTO student_cgpa
    FROM Students
    WHERE student_id = NEW.student_id;
    
    SELECT required_cgpa INTO job_min_cgpa
    FROM Jobs
    WHERE job_id = NEW.job_id;
    
    IF student_cgpa < job_min_cgpa THEN
        SET NEW.status = 'rejected';
    END IF;
END;
"""

STORED_PROC_SCRIPT = """
CREATE PROCEDURE GetStudentApplicationDetails(IN p_student_id INT)
BEGIN
    SELECT 
        a.application_id,
        j.title AS job_title,
        c.company_name,
        j.job_type,
        j.location,
        a.status AS application_status,
        a.applied_date
    FROM Applications a
    JOIN Jobs j ON a.job_id = j.job_id
    JOIN Companies c ON j.company_id = c.company_id
    WHERE a.student_id = p_student_id;
END;
"""

def create_triggers_and_procedures():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    try:
        cursor.execute("DROP TRIGGER IF EXISTS before_application_insert")
        cursor.execute("DROP PROCEDURE IF EXISTS GetStudentApplicationDetails")
        cursor.execute(TRIGGER_SCRIPT)
        cursor.execute(STORED_PROC_SCRIPT)
        conn.commit()
        print("Triggers and procedures created.")
    except mysql.connector.Error as e:
        print(f"Error creating triggers/procedures: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    create_triggers_and_procedures()
