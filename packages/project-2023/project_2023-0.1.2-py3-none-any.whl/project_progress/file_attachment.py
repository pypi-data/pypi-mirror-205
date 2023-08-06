import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


def send_email_with_attachment(send_email, send_pwd, smtp_name, smtp_port, recv_email, subject, text, file_path):
    """
    Send an email with an attachment using the given email information and attachment file.

    :param send_email: The sender's email address (str)
    :param send_pwd: The password used for authentication (str)
    :param smtp_name: The SMTP server name (str)
    :param smtp_port: The SMTP server port (int)
    :param recv_email: The recipient's email address (str)
    :param subject: The email subject (str)
    :param text: The email body (str)
    :param file_path: The path to the file to be attached (str)

    :return: None
    """
    msg = MIMEMultipart()

    msg["Subject"] = subject
    msg["From"] = send_email
    msg["To"] = recv_email

    contentPart = MIMEText(text)
    msg.attach(contentPart)

    with open(file_path, "rb") as f:
        etc_part = MIMEApplication(f.read())
        etc_part.add_header("Content-Disposition", "attachment", filename="sample_file.txt")
        msg.attach(etc_part)

    s = smtplib.SMTP(smtp_name, smtp_port)
    s.starttls()
    s.login(send_email, send_pwd)
    s.sendmail(send_email, recv_email, msg.as_string())
    s.quit()
