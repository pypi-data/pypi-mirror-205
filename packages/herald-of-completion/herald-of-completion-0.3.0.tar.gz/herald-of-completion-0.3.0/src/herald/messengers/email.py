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

import re
import smtplib
import ssl
from email.message import EmailMessage

from ..types import Messenger, Secrets, TaskInfo
from ..utils import build_arg_string, build_kwarg_string


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

        if (
            re.fullmatch(
                r"^[A-Za-z0-9._+\-\']+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$", recipient
            )
            is None
        ):
            raise ValueError("Invalid email address.")

    def set_secrets(self, secrets: Secrets) -> None:
        """Sets the secrets for the EmailMessenger.

        Secrets required are the SMTP details for the server that will be
        sending the email.

        Args:
            secrets: Secrets for the EmailMessenger.
        """
        self.smtp_server = secrets.smtp_server
        self.smtp_port = secrets.smtp_port
        self.smtp_starttls = secrets.smtp_starttls
        self.smtp_user = secrets.smtp_user
        self.smtp_password = secrets.smtp_password

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

        if info.send_args:
            args = build_arg_string(info.args)
            kwargs = build_kwarg_string(info.kwargs)
            call = f"{info.name}({args}, {kwargs})"
        else:
            call = f"{info.name}()"

        if info.message:
            msg_content = f"{info.message}\n"
        else:
            if info.has_errored:
                msg_content = "Task has failed with an error.\n"
            else:
                msg_content = "Task has completed successfully.\n"

        if info.send_function:
            msg_content += f"\n\nFunction:\n```\n{call}\n```"

        if info.send_result:
            msg_content += f"\n\nResult:\n```\n{info.result}\n```"

        msg.set_content(msg_content)

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
