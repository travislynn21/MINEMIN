import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests

class Notifications:
    def __init__(self, smtp_server, smtp_port, smtp_user, smtp_password, slack_webhook_url):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.slack_webhook_url = slack_webhook_url

    def send_email(self, recipient, subject, body):
        """Send an email notification."""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.smtp_user
            msg['To'] = recipient
            msg['Subject'] = subject

            msg.attach(MIMEText(body, 'plain'))

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)

            print(f"Email sent to {recipient}")
        except Exception as e:
            print(f"Failed to send email to {recipient}: {e}")

    def send_slack_message(self, message):
        """Send a Slack notification."""
        try:
            payload = {"text": message}
            response = requests.post(self.slack_webhook_url, json=payload)

            if response.status_code == 200:
                print("Slack message sent successfully.")
            else:
                print(f"Failed to send Slack message: {response.text}")
        except Exception as e:
            print(f"Failed to send Slack message: {e}")
