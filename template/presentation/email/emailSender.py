import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailSender:
    def __init__(self, smtp_server, smtp_port, email, email_pass):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email = email
        self.email_pass = email_pass

    def send_html_email(self, to_address, subject, message, is_html=False):
        msg = MIMEMultipart()
        msg['From'] = self.email
        msg['To'] = to_address
        msg['Subject'] = subject

        body = MIMEText(message, 'html' if is_html else 'plain')
        msg.attach(body)

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.email, self.email_pass)

            server.sendmail(self.email, to_address, msg.as_string())
