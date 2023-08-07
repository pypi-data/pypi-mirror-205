"""Defines all types, base classes, and dataclasses used in the package."""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Union


@dataclass
class Secrets:
    """Dataclass that holds all secrets needed for messengers.

    Args:
        webhook_url: A string containing the webhook url for a Discord messenger.
        smtp_server: A string containing the smtp server for an email messenger.
        smtp_port: An integer containing the smtp port for an email messenger.
        smtp_starttls: Boolean indicating whether to use starttls for an emails.
        smtp_user: A string containing the username for an email messenger.
        smtp_password: A string containing the password for an email messenger.
    """

    webhook_url: str = ""
    smtp_server: str = ""
    smtp_port: int = -1
    smtp_starttls: bool = True
    smtp_user: str = ""
    smtp_password: str = ""


@dataclass
class TaskInfo:
    """Dataclass that holds information about a task.

    An instance of this class is passed to the notify method of all messengers. \
    If creating a custom messenger, you can use these fields to construct a \
    notification message.

    Args:
        name: A string containing the name of the function being run.
        message: A string containing a custom message to be sent.
        send_result: Boolean indicating whether results should be sent.
        send_function: Boolean indicating whether calling function should be sent.
        send_args: Boolean indicating whether args and kwargs should be sent.
        args: Tuple containing the arguments passed to the function.
        kwargs: Dictionary containing the keyword arguments passed to the function.
        result: A string containing the return result of the function, or the traceback.
        header: A string containing a summary line for the notification header.
        has_errored: A boolean indicating whether the function raised an exception.
    """

    name: str = ""
    message: Union[str, None] = None
    send_result: bool = False
    send_function: bool = False
    send_args: bool = True
    args: tuple = ()
    kwargs: dict = field(default_factory=dict)
    result: str = ""
    header: str = ""
    has_errored: bool = False


class Messenger(ABC):
    """Abstract base class for all messengers."""

    @abstractmethod
    def set_secrets(self, secrets: Secrets) -> None:
        """Receive and set secrets used for the messenger.

        This method is abstract and must be implemented by all subclasses.

        Args:
            secrets: Secrets that need to be set for the messenger.
        """
        pass

    @abstractmethod
    def notify(self, info: TaskInfo) -> None:
        """Send a notification to the user.

        This method is abstract and must be implemented by all subclasses.

        Args:
            info: TaskInfo object containing information about the function that can \
            be used to construct the notification message.
        """
        pass
