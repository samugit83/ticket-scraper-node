
from mailer import send_email
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler
import requests

# Define the log file path
log_file_path = "/home/ubuntu/ticket-scraper/backend/logs/scrape.log"

# Set up the logger
logging.basicConfig(
    level=logging.INFO,  # Set the logging level
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log message format
    handlers=[
        RotatingFileHandler(log_file_path, maxBytes=1024*1024, backupCount=3),  # 1MB file size, keep 5 backups
        logging.StreamHandler()  # Also print logs to stdout (console)
    ]
)


logger = logging.getLogger(__name__)


def update_and_notify(matching_users):
    for user in matching_users:
        url = 'http://18.102.166.102/update_ticket_found'
        payload = {'_id': user['_id']}
        headers = {'Content-Type': 'application/json'}

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code != 200:
            logger.error(f"Failed to update ticket found for user {user['_id']}: {response.json().get('error', 'Unknown error')}")

        subject = 'Ticket available: ' + user['eventName']

        event_datetime = datetime.fromisoformat(user['eventIsoDatetime'])
        event_date_str = event_datetime.strftime('%a %d %B %Y').capitalize()

        html = f"""
        <html>
        <head></head>
        <body> 
            <h1>{user['eventName']}</h1>
            <p>Data dell'evento: {event_date_str}</p>
            <p>Città: {user['city'].capitalize()}</p>
            <p>Numero di biglietti: {user['nrTickets']}</p>
            <img src="{user['imgUrl']}" alt="Event Image" />
            <p><a href="{user['final_ticket_url']}">Acquista il biglietto</a></p>
        </body>
        </html>
        """

        email_addresses = user.get('emailList', [])
        for email in email_addresses:
            send_email(email, subject, html)

    return




