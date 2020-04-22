class RoleManager():

    def __init__(self):
        self.role_map = {}

    def register_bot_roles(self, bot, guild):
        for member in guild.members:
            if member.id == bot.user.id:
                break
        bot_guild_user = member
        # I'm pretty sure @everyone is always the first role
        bot_roles = bot_guild_user.roles[1:]
        self.role_map[guild.id] = [role.id for role in bot_roles]

    def get_available_roles(self, guild):
        """
        Gets the roles that the bot can add to the other users
        """
        roles = {}
        bot_roles_ids = self.role_map[guild.id]
        # We skip the first role, as it is @everyone
        for role in guild.roles[1:]:
            # We break out on the first role that the bot has, just to be safe
            if role.id in bot_roles_ids:
                break
            roles[role.name] = role.id
        return roles
