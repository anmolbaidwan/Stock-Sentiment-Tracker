import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

def process_alerts(alerts):
    for email in alerts:
        send_alert(email, alerts[email])

def send_alert(receiver_email, alertdata):
    msg = EmailMessage()
    msg['Subject'] = "Stock Tracker Alert"
    msg['From'] = "Noreply Alert <noreply.stocksentimenttracker@gmail.com>"
    msg['To'] = receiver_email
    content = "The Following Ticker(s) Have Experienced a Notable Change:\n"
    content += "------------------------------------------------------------\n"
    for entry in alertdata:
        content += f"Since: {entry['date']}\n"
        content += f"Ticker: {entry['ticker']}\n"
        if entry['close'] != 0:
            content+=f"Price has changed by: {entry['close']*100}%\n"
        if entry['sent'] != 0:
            content+=f"Sentiment has changed by: {entry['sent']*100}%\n"
        if entry['rec'] != 0:
            content+=f"Recommendation score has changed by: {entry['rec']*100}%\n"
        content += "------------------------------------------------------------\n"
    content += "Next alert for these tickers will be based on data from today's date."
    msg.set_content(content)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        pw = os.getenv("APP_PASSWORD")
        smtp.login('noreply.stocksentimenttracker@gmail.com', pw)
        smtp.send_message(msg)

def register_email(re, fname):
    msg = EmailMessage()
    msg['Subject'] = "Registration for StockSentimentTracker"
    msg['From'] = "Noreply Alert <noreply.stocksentimenttracker@gmail.com>"
    msg['To'] = re
    msg.set_content(f"This is an automated email to confirm {fname}'s registration for Stock Sentiment Tracker.\nPlease do not reply.")
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        pw = os.getenv("APP_PASSWORD")
        smtp.login('noreply.stocksentimenttracker@gmail.com', pw)
        smtp.send_message(msg)
        print("sent mail")

