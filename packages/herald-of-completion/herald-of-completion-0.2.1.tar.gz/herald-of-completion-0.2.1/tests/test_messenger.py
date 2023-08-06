from herald.decorators import Herald
from herald.messengers import DesktopMessenger, DiscordMessenger

herald = Herald(secrets="tests/test.env")


def test_desktop_has_no_secrets(mocker):
    desktop = DesktopMessenger()
    mocker.patch("herald.messengers.DesktopMessenger.notify", return_value=None)

    @herald(desktop)
    def get_list():
        x = [1, 2, 3]
        return x

    get_list()
    assert desktop.__dict__ == {}


def test_discord_has_url(mocker):
    discord = DiscordMessenger()
    mocker.patch("herald.messengers.DiscordMessenger.notify", return_value=None)

    @herald(discord)
    def get_list():
        x = [1, 2, 3]
        return x

    get_list()
    assert discord.webhook_url == "http://google.com"
