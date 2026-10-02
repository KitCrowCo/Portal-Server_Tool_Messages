import os
import requests

import smtplib
from email.message import EmailMessage

# from twilio.rest import Client

from fastapi import Form, HTTPException, BackgroundTasks
# from fastapi.responses import HTMLResponse, RedirectResponse
# from sqlalchemy.orm import Session
# from datetime import datetime, timedelta

# -- EMail --

# # Config
# FROM_EMAIL = os.getenv("AUCTION_EMAIL", "yourbusiness@gmail.com")
# API_URL = os.getenv("AUCTION_EMAIL_API_URL", "https://api.mailgun.net/v3")
# API_PASS = os.getenv("AUCTION_EMAIL_API_KEY", "APP_PASSWORD_HERE")

def send_email_direct(to, subject, body, config):
    """
    config is a dict containing:
    'type': 'api' or 'smtp'
    'url_or_host': SMTP host or API URL
    'port': SMTP port (optional)
    'user': API 'api' user or SMTP email
    'pass': API Key or SMTP Password
    'from': Sender email
    """
    try:
        if config['type'] == 'api':
            # Mailgun / API Logic
            return requests.post(config['url_or_host'], auth=(config['user'], config['pass']), data={"from": config['from'], "to": to, "subject": subject, "text": body})
        elif config['type'] == 'smtp':
            # Outlook / SMTP Logic
            msg = EmailMessage()
            msg.set_content(body)
            msg['Subject'] = subject
            msg['From'] = config['from']
            msg['To'] = ", ".join(to) if isinstance(to, list) else to
            # Typical for Office365: Port 587 + STARTTLS
            with smtplib.SMTP(config['url_or_host'], config.get('port', 587)) as server:
                server.starttls()  # Upgrade connection to secure
                server.login(config['user'], config['pass'])
                server.send_message(msg)
            return True
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Mail System Error: {str(e)}")

def send_email(to, subject, body, config): background_tasks.add_task(send_email_direct, to, subject, body, config)

# -- SMS --

# def twilio_check():
#     if TWILIO_TOKEN != "<token>":
#         client = Client(TWILIO_SID, TWILIO_TOKEN)
#         return True
#     return False

# def send_verification_sms(phone: str, code: str):
#     send_sms(phone, f"Auction verification code: {code} (expires in 30 min)")

def send_sms(phone: str, message: str):
    print("Not Yet Implemented")
    return False
    # client.messages.create(to=phone, from_=TWILIO_FROM, body=message)