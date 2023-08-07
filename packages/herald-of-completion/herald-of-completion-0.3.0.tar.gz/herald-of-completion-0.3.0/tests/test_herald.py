import pytest

from herald.decorators import Herald
from herald.types import Messenger, Secrets

herald = Herald(env="tests/test.env")


class DummyMessenger(Messenger):
    def __init__(self):
        self.secrets = None

    def set_secrets(self, secrets) -> None:
        self.secrets = secrets

    def notify(self, info) -> None:
        print(info)


def test_function_complete():
    @herald(DummyMessenger())
    def get_list():
        x = [1, 2, 3]
        return x

    get_list()


def test_function_error():
    @herald(DummyMessenger())
    def get_item():
        x = [1, 2, 3]
        return x[len(x) + 1]

    with pytest.raises(IndexError):
        get_item()


def test_secrets_are_loaded():
    assert isinstance(herald.secrets, Secrets)


def test_messenger_secrets_are_set():
    test_messenger = DummyMessenger()
    herald._set_messenger_secrets(test_messenger)
    assert test_messenger.secrets is not None
    assert test_messenger.secrets == herald.secrets
