import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv


load_dotenv()

usermail = os.getenv('GMAILUSER')
passgmailapp = os.getenv('PASSGMAILAPP')

# Function to send email
def send_email(email: str, subject: str = '', html: str = '') -> dict:
    try:
        # Setup the MIME
        message = MIMEMultipart()
        message['From'] = usermail
        message['To'] = email
        message['Subject'] = subject
        
        # Attach the HTML content to the email
        message.attach(MIMEText(html, 'html'))
        
        # Create a SMTP session
        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.starttls()  # Enable security
        
        # Login with the provided credentials
        session.login(usermail, passgmailapp)
        
        # Send the email
        response = session.sendmail(usermail, email, message.as_string())
        
        # Close the session
        session.quit()
        
        return {'ok': True, 'info': response}

    except Exception as error:
        return {'ok': False, 'info': str(error)}
    

