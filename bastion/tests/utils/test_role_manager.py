from bastion.utils.role_manager import RoleManager

from bastion.tests import MockBot, MockGuild, _everyone, _another_role, _some_role, _mock_bot_role


def test_register_bot_roles():
    manager = RoleManager()
    bot = MockBot()
    guild = MockGuild()

    manager.register_bot_roles(bot, guild)

    assert manager.role_map[guild.id] == [_mock_bot_role.id]


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
    guild.roles = [_everyone, _mock_bot_role, _some_role]
    manager.register_bot_roles(bot, guild)

    available_roles = manager.get_available_roles(guild)

    assert available_roles == []


