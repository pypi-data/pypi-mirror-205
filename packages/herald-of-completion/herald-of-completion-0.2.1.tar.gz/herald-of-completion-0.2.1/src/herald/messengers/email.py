"""Module for the Email messenger.

This module defines the Email messenger class, which is used to send
notifications via email.

Typical usage example:

.. code-block:: python
    
   from herald.decorators import Herald
   from herald.messengers import EmailMessenger

   herald = Herald(".env")
   email = EmailMessenger()

   @herald(email)
   def my_function():
      pass
"""

import smtplib
import ssl
from email.message import EmailMessage

from ..types import Messenger, TaskInfo


# TODO: validate email address. probably good to have an email type
class EmailMessenger(Messenger):
    """A class for sending notifications via email.

    Args:
        recipient: String containing the email address of the recipient.
        smtp_server: String containing the SMTP server address.
        smtp_port: Integer containing the SMTP server port.
        smtp_starttls: Boolean indicating whether to use STARTTLS.
        smtp_user: String containing the SMTP username.
        smtp_password: String containing the SMTP password.
    """

    def __init__(self, recipient: str):
        """Initializes the EmailMessenger with the given recipient.

        Args:
            recipient: String containing the email address of the recipient.
        """
        self.recipient: str = recipient
        self.smtp_server: str = ""
        self.smtp_port: int = -1
        self.smtp_starttls: bool = False
        self.smtp_user: str = ""
        self.smtp_password: str = ""

    def set_secrets(self, secrets: dict) -> None:
        """Sets the secrets for the EmailMessenger.

        Secrets required are the SMTP details for the server that will be
        sending the email.

        Args:
            secrets: A dictionary containing the secrets for the EmailMessenger.
        """
        self.smtp_server = secrets["SMTP_SERVER"]
        self.smtp_port = secrets["SMTP_PORT"]
        self.smtp_starttls = secrets["SMTP_STARTTLS"]
        self.smtp_user = secrets["SMTP_USER"]
        self.smtp_password = secrets["SMTP_PASSWORD"]

    def notify(self, info: TaskInfo) -> None:
        """Creates and sends an email with the given TaskInfo.

        Args:
            info: TaskInfo object containing the information to be \
            sent. Contents should be used to create the email.

        Raises:
            SMTPException: An error occurred while sending the email.
        """
        msg = EmailMessage()
        msg["Subject"] = f"{info.header}"
        msg.set_content(f"{info.message}\n\n{info.result}")

        context = ssl.create_default_context()
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            try:
                server.ehlo()
                if self.smtp_starttls:
                    server.starttls(context=context)
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg, self.smtp_user, self.recipient)
            except smtplib.SMTPException as e:
                raise e
