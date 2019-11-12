class MockCtx():

    def __init__(self, invoked_subcommand=None):
        self.invoked_subcommand = None


class MockRole():
    _id = 500

    def __init__(self, name):
        self.name = name
        self.id = MockRole._id
        MockRole._id += 1

_everyone = MockRole('@everyone')
_mock_bot_role = MockRole('MockBot')
_some_role = MockRole('some_role')
_another_role = MockRole('another_role')

class MockUser():
    def __init__(self):
        self.id = 100


class MockBot():
    def __init__(self):
        self.id = 1
        self.user = MockUser()
        self.roles = [_everyone, _mock_bot_role]


class MockGuild():
    def __init__(self):
        self.id = 1000
        self.members = [MockBot()]
        self.roles = [_everyone, _some_role, _another_role, _mock_bot_role, MockRole('after_role')]
