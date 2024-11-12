import pymysql.cursors
import streamlit as st
from db.queries import get_database_connection
from notifications.email import send_application_status_email
from mysql.connector import Error
import pymysql
from pymysql import MySQLError

def manage_company_profile():
    st.subheader("Company Details")
    conn = None
    cursor = None
    
    try:
        conn = get_database_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        # Fetch existing details based on the user_id
        cursor.execute("SELECT * FROM Companies WHERE user_id = %s", (st.session_state.user_id,))
        company = cursor.fetchall()  # Use fetchall() to ensure all results are consumed
        
        if not company:
            st.error("No company details found. Please ensure you are logged in as a company.")
            return
            
        company = company[0]  # Get the first (and should be only) result
        
        # Pre-fill the form with existing company data
        company_name = st.text_input("Company Name", company['company_name'])
        industry = st.text_input("Industry", company['industry'])
        website = st.text_input("Website", company['website'])
        description = st.text_area("Description", company['description'])

        if st.button("Update Company Profile"):
            update_query = """
                UPDATE Companies 
                SET company_name = %s, 
                    industry = %s, 
                    website = %s, 
                    description = %s 
                WHERE user_id = %s
            """
            cursor.execute(update_query, 
                         (company_name, industry, website, description, st.session_state.user_id))
            conn.commit()
            st.success("Company profile updated successfully!")

    except MySQLError as e:
        st.error(f"Database error: {str(e)}")
    finally:
        if cursor:
            cursor.fetchall()  # Consume any remaining results
            cursor.close()
        if conn:
            conn.close()

def post_job():
    st.subheader("Post a Job")
    conn = None
    cursor = None
    
    try:
        conn = get_database_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        # Get company ID
        cursor.execute("SELECT company_id FROM Companies WHERE user_id = %s", 
                       (st.session_state.user['user_id'],))
        company_data = cursor.fetchall()  # Use fetchall() to ensure all results are consumed
        
        if not company_data:
            st.error("Company profile not found.")
            return
        
        company_id = company_data[0]['company_id']
        
        title = st.text_input("Job Title")
        description = st.text_area("Job Description")
        job_type = st.selectbox("Job Type", ["internship", "fulltime"])
        location = st.text_input("Location")
        salary_range = st.text_input("Salary Range")
        required_cgpa = st.number_input("Minimum CGPA", min_value=0.0, max_value=10.0)
        deadline = st.date_input("Application Deadline")

        if st.button("Post Job"):
            # Check for existing job with same details
            check_query = """
                SELECT * FROM Jobs 
                WHERE company_id = %s 
                AND title = %s 
                AND description = %s 
                AND job_type = %s 
                AND location = %s
            """
            cursor.execute(check_query, 
                           (company_id, title, description, job_type, location))
            existing_job = cursor.fetchone()

            if existing_job:
                st.warning("A job with the same title, description, job type, and location already exists.")
            else:
                # Insert the new job since no duplicate was found
                insert_query = """
                    INSERT INTO Jobs (
                        company_id, title, description, job_type, 
                        location, salary_range, required_cgpa, deadline
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, 
                               (company_id, title, description, job_type, 
                                location, salary_range, required_cgpa, deadline))
                conn.commit()
                st.success("Job posted successfully!")
    
    except MySQLError as e:
        st.error(f"Database error: {str(e)}")
    finally:
        if cursor:
            cursor.fetchall()  # Consume any remaining results
            cursor.close()
        if conn:
            conn.close()


def manage_applications():
    st.subheader("Manage Applications")
    conn = None
    cursor = None
    
    try:
        conn = get_database_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        # Get company ID
        cursor.execute("SELECT company_id FROM Companies WHERE user_id = %s", 
                      (st.session_state.user['user_id'],))
        company_data = cursor.fetchall()  # Use fetchall() to ensure all results are consumed
        
        if not company_data:
            st.error("Company profile not found.")
            return
            
        company_id = company_data[0]['company_id']
        
        # Fetch applications
        cursor.execute("""
            SELECT 
                a.application_id,
                s.first_name,
                s.last_name,
                s.student_id,
                j.title,
                a.status
            FROM Applications a
            JOIN Students s ON a.student_id = s.student_id
            JOIN Jobs j ON a.job_id = j.job_id
            WHERE j.company_id = %s
        """, (company_id,))
        
        applications = cursor.fetchall()
        
        if not applications:
            st.info("No applications found.")
            return
            
        for app in applications:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"""
                    **Applicant:** {app['first_name']} {app['last_name']}  
                    **Job:** {app['title']}  
                    **Current Status:** {app['status']}
                """)
            
            with col2:
                new_status = st.selectbox(
                    "Update Status",
                    ["pending", "shortlisted", "rejected", "accepted"],
                    index=["pending", "shortlisted", "rejected", "accepted"].index(app['status']),
                    key=f"status_{app['application_id']}"
                )
                
                if st.button("Update", key=f"update_{app['application_id']}"):
                    cursor.execute(
                        "UPDATE Applications SET status = %s WHERE application_id = %s",
                        (new_status, app['application_id'])
                    )
                    conn.commit()
                    send_application_status_email(
                        app['student_id'],
                        app['title'],
                        new_status
                    )
                    st.success(f"Status updated to {new_status}!")

    except MySQLError as e:
        st.error(f"Database error: {str(e)}")
    finally:
        if cursor:
            cursor.fetchall()  # Consume any remaining results
            cursor.close()
        if conn:
            conn.close()

def company_dashboard():
    st.title("Company Dashboard")
    
    tab1, tab2, tab3 = st.tabs(["Manage Profile", "Post Jobs", "Manage Applications"])
    
    with tab1:
        manage_company_profile()
    with tab2:
        post_job()
    with tab3:
        manage_applications()
