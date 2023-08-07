import pytest

from herald.decorators import Herald
from herald.messengers import (DesktopMessenger, DiscordMessenger,
                               EmailMessenger)
from herald.types import Secrets

herald = Herald(env="tests/test.env")


def test_desktop_has_no_secrets(mocker):
    desktop = DesktopMessenger()
    mocker.patch("herald.messengers.DesktopMessenger.notify", return_value=None)

    @herald(desktop)
    def get_list():
        x = [1, 2, 3]
        return x

    get_list()
    assert desktop.__dict__ == {}


def test_email_address_correct():
    _ = EmailMessenger("user@email.com")
    _ = EmailMessenger("user-name@email.address.com")


def test_email_address_incorrect():
    with pytest.raises(ValueError):
        _ = EmailMessenger("useremail.com")

    with pytest.raises(ValueError):
        _ = EmailMessenger("user@emailcom")


def test_discord_has_url(mocker):
    discord = DiscordMessenger()
    mocker.patch("herald.messengers.DiscordMessenger.notify", return_value=None)

    @herald(discord)
    def get_list():
        pass

    get_list()
    assert discord.webhook_url == "https://discord.com/api/webhooks/123123/test"


def test_discord_url_correct():
    discord = DiscordMessenger()
    discord.set_secrets(Secrets(webhook_url="http://discord.com/api/webhooks/12"))
    discord.set_secrets(Secrets(webhook_url="https://discord.com/api/webhooks/12"))


def test_discord_url_incorrect():
    discord = DiscordMessenger()

    with pytest.raises(ValueError):
        discord.set_secrets(Secrets(webhook_url="https://discord.com/api/webhooks"))

    with pytest.raises(ValueError):
        discord.set_secrets(Secrets(webhook_url="discord.com/api/webhooks/12"))
