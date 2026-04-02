import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv

def send_alert(receiver_email, ticker):
    msg = EmailMessage()
    msg['Subject'] = "Stock Alert Update"
    msg['From'] = "Noreply Alert <your_email@gmail.com>"
    msg['To'] = receiver_email
    msg.set_content(f"This is an automated alert for {ticker} Please do not reply.")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        pw = os.getenv("APP_PASSWORD")
        smtp.login('noreply.stocksentimenttracker@gmail.com', pw)
        smtp.send_message(msg)
