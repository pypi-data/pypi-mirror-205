"""Defines all types, base classes, and dataclasses used in the package."""
from abc import ABC, abstractmethod
from dataclasses import dataclass

# NOTE: dataclass for secrets?


@dataclass
class TaskInfo:
    """Dataclass that holds information about a task.

    Args:
        name: A string containing the name of the function being run.
        header: A string containing a summary line for the notification header.
        message: A string containing the main body of the notification message.
        result: A string containing the return result of the function, or the traceback.
        has_errored: A boolean indicating whether the function raised an exception.
    """

    name: str
    header: str
    message: str = ""
    result: str = ""
    has_errored: bool = False


class Messenger(ABC):
    """Abstract base class for all messengers."""

    @abstractmethod
    def set_secrets(self, secrets: dict) -> None:
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
