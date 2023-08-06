"""Module for the Desktop messenger.

This module defines the Desktop messenger class, which is used to send
OS-native desktop notifications.

Typical usage example:

.. code-block:: python

   from herald.decorators import Herald
   from herald.messengers import DesktopMessenger

   herald = Herald(".env")
   desktop = DesktopMessenger()

   @herald(desktop)
   def my_function():
       pass
"""
from plyer import notification

from ..types import Messenger, TaskInfo


class DesktopMessenger(Messenger):
    """A class used to send OS-native desktop notifications."""

    def __init__(self):
        """Initializes the DesktopMessenger class."""
        pass

    def set_secrets(self, secrets: dict) -> None:
        """Sets the secrets for the DesktopMessenger class.

        Must be implemented as a result of inheriting from the Messenger class. \
        However, the DesktopMessenger itself does not require any secrets.

        Args:
            secrets: A dictionary of secrets to be used by the messenger.
        """
        pass

    def notify(self, info: TaskInfo) -> None:
        """Constructs and sends a desktop notification using the function information.

        Args:
            info: TaskInfo object containing information about the function. \
            Contents should be used to construct the notification message.
        """
        opts = {
            "title": info.header,
            "message": info.message,
            "timeout": 10,
        }
        notification.notify(**opts)
