"""Helper functions used throughout the package."""

from typing import List, TypeVar, Union

from dotenv import dotenv_values

from .types import Messenger, Secrets, TaskInfo

T = TypeVar("T")


def truncate(input: T, length: int) -> Union[T, str]:
    """Truncate an input value to custom typed representation.

    Args:
        input: Value to be truncated. Can be of any type.
        length: Length to truncate the value to.

    Returns:
        Truncated representation of the input.
    """
    if isinstance(input, bool) or isinstance(input, type(None)):
        return input

    input_type = type(input).__name__
    try:
        input_clean = str(input).strip().replace("\n", " ")
    except Exception:
        return input_type

    if len(input_clean) > length:
        half_len = length // 2
        start = input_clean[:half_len]
        end = input_clean[-half_len:]
        output = f"{start}..<{input_type}>..{end}"
    else:
        output = input

    return output


def build_arg_string(args: tuple, truncate_length: int = 10) -> str:
    """Create string representation of an args tuple.

    Args:
        args: Tuple of arguments to be converted to a string.
        truncate_length: Length to truncate the string to.

    Returns:
        String representation of the args.
    """
    result = ""
    for arg in args:
        truncated = truncate(arg, truncate_length)
        if isinstance(arg, str):
            result += f"'{truncated}', "
        else:
            result += f"{truncated}, "
    result = result[:-2]  # remove last comma
    return result


def build_kwarg_string(kwargs: dict, truncate_length: int = 10) -> str:
    """Create string representation of a kwargs dict.

    Args:
        kwargs: Dictionary of keyword arguments to be converted to a string.
        truncate_length: Length to truncate the string to.

    Returns:
        String representation of the kwargs dict.
    """
    result = ""
    for key, value in kwargs.items():
        truncated = truncate(value, truncate_length)
        if isinstance(value, str):
            result += f"{key}='{truncated}', "
        else:
            result += f"{key}={truncated}, "
    result = result[:-2]  # remove last comma
    return result


def load_secrets(env: str = ".env") -> Secrets:
    """Load secrets from a .env file.

    The contents of the .env file are stored in a Secrets object.

    Args:
        env: Path to the .env file.
    """
    try:
        env_dict = dotenv_values(env)
        lowered = {k.lower(): v for k, v in env_dict.items()}
        secrets = Secrets(**lowered)
    except FileNotFoundError:
        secrets = Secrets()

    return secrets


def send_notification(
    messengers: Union[Messenger, List[Messenger]], info: TaskInfo, env: str = ".env"
) -> None:
    """Send notification without using a decorator.

    This function can be used to send a notification without using a decorator. This \
    allows you to send a notification at any point, without tying it to a specific \
    function.

    Args:
        messengers: Messenger, or list of Messenger, that will send the notification.
        info: TaskInfo object containing information to send in the notification.
        env: Path to the .env file containing the secrets to use.
    """
    secrets = load_secrets(env)

    if isinstance(messengers, list):
        for messenger in messengers:
            messenger.set_secrets(secrets)
            messenger.notify(info)
    else:
        messengers.set_secrets(secrets)
        messengers.notify(info)
