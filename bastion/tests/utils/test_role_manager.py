from bastion.utils.role_manager import RoleManager


class MockRole():
    _id = 500

    def __init__(self, name):
        self.name = name
        self.id = MockRole._id
        MockRole._id += 1

_everyone = MockRole('@everyone')
_mock_bot = MockRole('MockBot')
_some_role = MockRole('some_role')
_another_role = MockRole('another_role')

class MockUser():
    def __init__(self):
        self.id = 100


class MockBot():
    def __init__(self):
        self.id = 1
        self.user = MockUser()
        self.roles = [_everyone, _mock_bot]


class MockGuild():
    def __init__(self):
        self.id = 1000
        self.members = [MockBot()]
        self.roles = [_everyone, _some_role, _another_role, _mock_bot, MockRole('after_role')]


def test_register_bot_roles():
    manager = RoleManager()
    bot = MockBot()
    guild = MockGuild()

    manager.register_bot_roles(bot, guild)

    assert manager.role_map[guild.id] == [_mock_bot.id]


def test_get_available_roles():
    manager = RoleManager()
    bot = MockBot()
    guild = MockGuild()
    manager.register_bot_roles(bot, guild)

    available_roles = manager.get_available_roles(guild)

    assert available_roles == [_some_role, _another_role]


def test_get_available_roles_may_return_empty():
    manager = RoleManager()
    bot = MockBot()
    guild = MockGuild()
    guild.roles = [_everyone, _mock_bot, _some_role]
    manager.register_bot_roles(bot, guild)

    available_roles = manager.get_available_roles(guild)

    assert available_roles == []


