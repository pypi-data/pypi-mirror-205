"""Main module containing the decorator definition.

This module and class should be imported and used to create a new decorator instance.

Typical usage example:

.. code-block:: python

   from herald.decorators import Herald

   herald = Herald(".env")

   @herald(...)
   def my_function():
       pass
"""
import traceback
from functools import wraps
from typing import Any, Callable, List, Union

from .types import Messenger, Secrets, TaskInfo
from .utils import load_secrets


class Herald:
    """Class for creating a decorator instance.

    This class is used to set up the decorator with the .env file. \
    The resulting decorator can be used to decorate long-running functions.

    Args:
        secrets: Secrets object containing the secrets from the .env file.
    """

    def __init__(self, env: str = ".env"):
        """Initializes the instance with the .env file.

        Args:
            env: String containing the path to the .env file.
        """
        self.secrets: Secrets = load_secrets(env)

    def __call__(
        self,
        messengers: Union[Messenger, List[Messenger]],
        message: Union[str, None] = None,
        send_result: bool = True,
        send_function: bool = True,
        send_args: bool = True,
    ) -> Callable:
        """Creates a decorator instance with the given messengers.

        Args:
            messengers: Messenger, or list of Messenger, to send the messages.
            message: String containing a custom message to send.
            send_result: Boolean indicating whether to send the result of the function.
            send_function: Boolean indicating whether to send the name of the original \
            calling function.
            send_args: Boolean indicating whether to send the args and kwargs that \
            were passed to the function.

        Returns:
            A decorator instance that can be used to wrap functions.
        """

        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args: Any, **kwargs: Any):
                info = TaskInfo(
                    name=func.__name__,
                    message=message,
                    send_result=send_result,
                    send_function=send_function,
                    send_args=send_args,
                    header="Herald: Task Status",
                    args=args,
                    kwargs=kwargs,
                )

                try:
                    result = func(*args, **kwargs)
                    info.has_errored = False
                    info.result = str(result)
                    self._notify_messengers(messengers, info)
                    return result
                except Exception as e:
                    info.has_errored = True
                    info.result = str(traceback.format_exc())
                    self._notify_messengers(messengers, info)
                    raise e

            return wrapper

        return decorator

    def _notify_messengers(
        self, messengers: Union[Messenger, List[Messenger]], info: TaskInfo
    ) -> None:
        """Iterate through the messengers and ask them to send the notification.

        This is an internal method and should not be called directly.

        Args:
            messengers: Messenger, or list of Messenger, to notify.
            info: TaskInfo to send to the messengers.
        """
        if isinstance(messengers, list):
            for messenger in messengers:
                self._set_messenger_secrets(messenger)
                messenger.notify(info)
        else:
            self._set_messenger_secrets(messengers)
            messengers.notify(info)

    def _set_messenger_secrets(self, messenger: Messenger) -> None:
        """Tells the messenger to set the secrets from the .env file.

        This is an internal method and should not be called directly.

        Args:
            messenger: Messenger to set the secrets for.
        """
        messenger.set_secrets(self.secrets)
