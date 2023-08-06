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


def read_email_titles(imap, num_emails=5):
    """
    Read the email titles from an IMAP mailbox.

    :param imap: An IMAP object connected to the mailbox (IMAP object)
    :param num_emails: The number of email titles to read (int), default is 5
    :return: A list of email title information (list)
    """
    email_titles = []

    imap.select("INBOX")
    resp, data = imap.uid("search", None, "All")
    all_email = data[0].split()
    last_email = all_email[-num_emails:]

    for mail in reversed(last_email):
        result, data = imap.uid("fetch", mail, "(RFC822)")
        raw_email = data[0][1]
        email_message = email.message_from_bytes(raw_email, policy=policy.default)

        subject, encode = find_encoding_info(email_message["Subject"])
        email_titles.append(
            (email_message["From"], email_message["Sender"], email_message["To"], email_message["Date"], subject)
        )

    return email_titles
