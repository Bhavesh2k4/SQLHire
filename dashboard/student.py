import streamlit as st
from db.queries import get_database_connection
import pandas as pd
from mysql.connector import Error
import pymysql
from pymysql import MySQLError

def manage_profile():
    st.subheader("Personal Details")
    conn = get_database_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # Fetch existing details based on the user_id
    cursor.execute("SELECT * FROM Students WHERE user_id = %s", (st.session_state.user_id,))
    student = cursor.fetchone()

    if student:
        # If student details are found, pre-fill the form with their existing data
        first_name = st.text_input("First Name", student['first_name'])
        last_name = st.text_input("Last Name", student['last_name'])
        email = st.text_input("Email", student['email'])
        phone = st.text_input("Phone Number", student['phone'])
        cgpa = st.number_input("CGPA", min_value=0.0, max_value=10.0, value=float(student['cgpa']))
        graduation_year = st.number_input("Graduation Year", min_value=2020, max_value=2100, value=student['graduation_year'])
        department = st.text_input("Department", student['department'])
    else:
        st.error("No student details found. Please ensure you are logged in as a student.")
        return

    if st.button("Update Profile"):
        cursor.execute("""
            UPDATE Students
            SET first_name=%s, last_name=%s, email=%s, phone=%s, cgpa=%s, graduation_year=%s, department=%s
            WHERE user_id=%s
        """, (first_name, last_name, email, phone, cgpa, graduation_year, department, st.session_state.user_id))
        conn.commit()
        st.success("Profile updated successfully.")

    cursor.close()
    conn.close()


def manage_skills():
    st.subheader("Skills Management")
    
    conn = get_database_connection()
    if not conn:
        st.error("Database connection failed")
        return
        
    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        
        # Get student_id using user_id
        cursor.execute("SELECT student_id FROM Students WHERE user_id = %s", (st.session_state.user['user_id'],))
        student_data = cursor.fetchone()
        
        if not student_data:
            st.error("Student profile not found.")
            return
        
        student_id = student_data['student_id']
        
        # Display existing skills
        cursor.execute("""
            SELECT skill_name, proficiency_level 
            FROM Student_Skills 
            WHERE student_id = %s
            ORDER BY skill_name
        """, (student_id,))
        
        existing_skills = cursor.fetchall()
        
        if existing_skills:
            st.write("Your Current Skills:")
            skills_df = pd.DataFrame(existing_skills)
            
            # Add a checkbox for each skill to select for deletion
            skill_to_delete = []
            
            for skill in existing_skills:
                if st.checkbox(f"Delete {skill['skill_name']}", key=f"del_{skill['skill_name']}"):
                    skill_to_delete.append(skill['skill_name'])

            # Show the skills in a table
            st.dataframe(skills_df)

            # Delete selected skills
            if skill_to_delete and st.button("Remove Selected Skills"):
                for skill_name in skill_to_delete:
                    cursor.execute("""
                        DELETE FROM Student_Skills 
                        WHERE student_id = %s AND skill_name = %s
                    """, (student_id, skill_name))
                
                conn.commit()
                st.success("Selected skills removed successfully!")
                st.experimental_rerun()

        
        # Add multiple skills
        st.write("Add New Skills:")
        
        # Create a container for multiple skills
        num_skills = st.number_input("Number of skills to add", min_value=1, max_value=10, value=1)
        
        with st.form("add_skills_form"):
            new_skills = []
            for i in range(num_skills):
                col1, col2 = st.columns(2)
                with col1:
                    skill = st.text_input(f"Skill {i+1}", key=f"skill_{i}")
                with col2:
                    proficiency = st.selectbox(
                        f"Proficiency {i+1}",
                        ["beginner", "intermediate", "advanced"],
                        key=f"prof_{i}"
                    )
                if skill:  # Only add non-empty skills
                    new_skills.append((skill, proficiency))
            
            submit = st.form_submit_button("Add Skills")
            
            if submit and new_skills:
                try:
                    # Check for duplicates before inserting
                    for skill, proficiency in new_skills:
                        cursor.execute("""
                            SELECT COUNT(*) 
                            FROM Student_Skills 
                            WHERE student_id = %s AND skill_name = %s
                        """, (student_id, skill))
                        
                        if cursor.fetchone()['COUNT(*)'] == 0:
                            cursor.execute("""
                                INSERT INTO Student_Skills 
                                (student_id, skill_name, proficiency_level) 
                                VALUES (%s, %s, %s)
                            """, (student_id, skill, proficiency))
                            
                    conn.commit()
                    st.success("Skills added successfully!")
                    st.experimental_rerun()
                except Error as e:
                    st.error(f"Error adding skills: {e}")
    except MySQLError as e:
        st.error(f"Database error: {e}")
    finally:
        cursor.close()
        conn.close()

def view_jobs():
    st.subheader("Available Jobs")
    conn = get_database_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT student_id FROM Students WHERE user_id = %s", (st.session_state.user['user_id'],))
    student_data = cursor.fetchone()
        
    if not student_data:
        st.error("Student profile not found.")
        return
        
    student_id = student_data['student_id']
    cursor.execute("SELECT * FROM Jobs WHERE status='open'")
    jobs = cursor.fetchall()
    for job in jobs:
        st.write(job)
        if st.button("Apply", key=job['job_id']):
            cursor.execute("INSERT INTO Applications (student_id, job_id) VALUES (%s, %s)", 
                           (student_id, job['job_id']))
            conn.commit()
            st.success(f"Applied for {job['title']}.")
    cursor.close()
    conn.close()

def view_applications():
    st.subheader("Application Status")
    conn = get_database_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT student_id FROM Students WHERE user_id = %s", (st.session_state.user['user_id'],))
    student_data = cursor.fetchone()
        
    if not student_data:
        st.error("Student profile not found.")
        return
        
    student_id = student_data['student_id']
    cursor.execute("""
        CALL GetStudentApplicationDetails(%s)
    """, (student_id,))
    applications = cursor.fetchall()
    st.write(applications)
    cursor.close()
    conn.close()

def student_dashboard():
    st.title("Student Dashboard")
    
    tab1, tab2, tab3 = st.tabs(["Profile", "Jobs", "Applications"])
    with tab1:
        manage_profile()
        manage_skills()
    with tab2:
        view_jobs()
    with tab3:
        view_applications()
