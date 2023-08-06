"""
A package for working with email notifications and integrations.

This package provides functions for sending emails, attaching files,
reading email titles and contents, sending notifications based on
specific email criteria, and interacting with the Slack API through
webhooks.
"""
from .email_sending import *
from .file_attachment import *
from .reading_email_content import *
from .reading_email_title import *
from .send_notification import *
from .slack_bot import *

__version__ = "0.1.1"
