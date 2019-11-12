from unittest.mock import patch, Mock

from bastion import init_bastion, BastionBot
from bastion.commands import Track, Misc, Roles

def test_init_bastion():
    token = 'TOKEN'
    config = {
        'client': {
            'token': token
        }
    }

    bastion = init_bastion(config)

    assert bastion.token == token
    assert {Track, Misc, Roles} == {cog.__class__ for cog in bastion.cogs.values()}


@patch('bastion.Bot.run')
def test_discord_run_is_called_with_token(run_mock):
    token = 'TOKEN'
    config = {
        'client': {
            'token': token
        }
    }

    bastion = init_bastion(config)
    bastion.run()

    run_mock.assert_called_once_with(bastion.token)
