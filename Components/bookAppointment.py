import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

def send_email(receiver_email, patient_name):
    # Email configuration
    sender_email = "dimpal21_ug@cse.nits.ac.in"
    password = os.getenv("EMAIL_PASSWORD")
    subject = "Booking a Slot for Visit"

    # Email content
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    body = f"Dear Dr.,\n\nPatient {patient_name} wants to book a medical appointment with you.\n\nBest regards,\nALLisWell"

    message.attach(MIMEText(body, "plain"))

    # SMTP server configuration
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    try:
        # Establish a secure connection with the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, password)

        # Send the email
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully!")

    except Exception as e:
        print(f"An error occurred while sending the email: {str(e)}")

    finally:
        # Close the connection to the SMTP server
        server.quit()

