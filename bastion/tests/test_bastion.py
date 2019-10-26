from bastion import init_bastion
from bastion.commands import Track, Misc, Roles

def test_init_bastion():
    token = 'TOKEN'
    config = {
        'client': {
            'token': token
        }
    }

    bastion = init_bastion(config)

    assert bastion.http.token == token
    for command in {Track, Misc, Roles}:
        assert command in bastion.cogs.values()
