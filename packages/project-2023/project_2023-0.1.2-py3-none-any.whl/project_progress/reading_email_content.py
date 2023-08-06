import email
from email import policy


def find_encoding_info(txt):
    """
    Find encoding information for a given text.

    :param txt: The text to find encoding information for (str)
    :return: A tuple containing the decoded subject and the encoding (tuple)
    """
    info = email.header.decode_header(txt)
    subject, encode = info[0]
    return subject, encode


def read_email_contents(imap, num_emails=5):
    """
    Read the email contents from an IMAP mailbox.

    :param imap: An IMAP object connected to the mailbox (IMAP object)
    :param num_emails: The number of email contents to read (int), default is 5
    :return: A list of email content information (list)
    """
    email_contents = []

    imap.select("INBOX")
    resp, data = imap.uid("search", None, "All")
    all_email = data[0].split()
    last_email = all_email[-num_emails:]

    for mail in reversed(last_email):
        result, data = imap.uid("fetch", mail, "(RFC822)")
        raw_email = data[0][1]
        email_message = email.message_from_bytes(raw_email, policy=policy.default)

        subject, encode = find_encoding_info(email_message["Subject"])

        message = ""
        if email_message.is_multipart():
            for part in email_message.get_payload():
                if part.get_content_type() == "text/plain":
                    bytes = part.get_payload(decode=True)
                    encode = part.get_content_charset()
                    message = message + str(bytes, encode)

        email_contents.append(
            (
                email_message["From"],
                email_message["Sender"],
                email_message["To"],
                email_message["Date"],
                subject,
                message,
            )
        )

    return email_contents
