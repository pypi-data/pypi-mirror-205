"""Module for the Discord messenger.

This module defines the Discord messenger class, which is used to send
notifications using Discord webhooks to specific servers and channels.

Typical usage example:

.. code-block:: python
    
   from herald.decorators import Herald
   from herald.messengers import DiscordMessenger

   herald = Herald(".env")
   discord = DiscordMessenger()

   @herald(discord)
   def my_function():
       pass
"""

import re

import requests

from ..types import Messenger, Secrets, TaskInfo
from ..utils import build_arg_string, build_kwarg_string


class DiscordMessenger(Messenger):
    """A class used to send Discord notifications.

    The webhook URL can be obtained from the server settings inside Discord. \
    You can find instructions on how to do this here: \
    https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks

    Args:
        webhook_url: String containing the URL for the Discord webhook.
    """

    def __init__(self):
        """Initializes the DiscordMessenger class."""
        self.webhook_url: str = ""

    def set_secrets(self, secrets: Secrets) -> None:
        """Sets the secrets for the DiscordMessenger class.

        The only secret required is the webhook URL.

        Args:
            secrets: Secrets to be used by the messenger.
        """
        url = secrets.webhook_url
        if re.fullmatch(r"^http[s]?:\/\/discord.com\/api\/webhooks\/.*$", url) is None:
            raise ValueError("Invalid webhook url.")
        else:
            self.webhook_url = url

    def notify(self, info: TaskInfo) -> None:
        """Constructs and sends a Discord notification.

        Args:
            info: TaskInfo object containing information about the task that was run. \
            Contents should be used to construct the notification.

        Raises:
            HTTPError: An error occurred while making the HTTP request.
        """
        msg_content = f"**{info.header}**\n"

        if info.send_args:
            args = build_arg_string(info.args)
            kwargs = build_kwarg_string(info.kwargs)
            call = f"{info.name}({args}, {kwargs})"
        else:
            call = f"{info.name}()"

        if info.message:
            msg_content += f"{info.message}\n"
        else:
            if info.has_errored:
                msg_content += "Task has failed with an error.\n"
            else:
                msg_content += "Task has completed successfully.\n"

        if info.send_function:
            msg_content += f"\nFunction:\n```{call}```"

        if info.send_result:
            msg_content += f"\nResult:\n```{info.result}```"

        data = {
            "content": msg_content,
        }

        result = requests.post(self.webhook_url, json=data)

        try:
            result.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise e
