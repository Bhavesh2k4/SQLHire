import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from db.queries import get_student_email
import os
from dotenv import load_dotenv

load_dotenv()
EMAIL=os.getenv('EMAIL')
PASSWORD=os.getenv('EMAIL_PASSWORD')
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def send_application_status_email(student_id, job_title, status):
    to_email = get_student_email(student_id)
    if not to_email:
        return
    
    subject = f"Application Status Update for {job_title}"
    body = f"Dear Student,\n\nYour application status for the job '{job_title}' has been updated to: {status}.\n\nBest Regards,\nPlacement System"
    
    msg = MIMEMultipart()
    msg["From"] = EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL, PASSWORD)
            server.sendmail(EMAIL, to_email, msg.as_string())
    except Exception as e:
        print(f"Failed to send email: {e}")
