import smtplib
from email.mime.text import MIMEText


def send_email(email_info):
    """
    Send an email using the given email information.

    :param email_info: A dictionary containing the following keys:
        - "text": The email body (str)
        - "Subject": The email subject (str)
        - "From": The sender's email address (str)
        - "To": The recipient's email address (str)
        - "send_email": The email address used for authentication (str)
        - "send_pwd": The password used for authentication (str)
        - "smtp_name" (optional): The SMTP server name (str). Default is "smtp.example.com".
        - "smtp_port" (optional): The SMTP server port (int). Default is 587.

    :return: None
    """
    msg = MIMEText(email_info["text"])

    msg["Subject"] = email_info["Subject"]
    msg["From"] = email_info["From"]
    msg["To"] = email_info["To"]

    smtp_name = email_info.get("smtp_name", "smtp.example.com")
    smtp_port = email_info.get("smtp_port", 587)

    s = smtplib.SMTP(smtp_name, smtp_port)
    s.starttls()
    s.login(email_info["send_email"], email_info["send_pwd"])
    s.send_message(msg)
    s.quit()
