import smtplib
from email.mime.text import MIMEText

# Configure your email credentials and recipient
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "your_email@gmail.com"          # Your email
EMAIL_PASSWORD = "your_email_app_password"      # Use app password, not your regular Gmail password
ALERT_RECIPIENT = "admin_email@example.com"     # Who will get the alerts

def send_email_alert(subject, message):
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = ALERT_RECIPIENT

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("Alert email sent successfully!")
    except Exception as e:
        print(f"Failed to send alert email: {e}")
