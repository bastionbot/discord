from discord.ext import commands as discord_commands
from discord.ext.commands import Bot


class BastionBot(Bot):

    def __init__(self, config, *args, **kwargs):
        self.token = config['client']['token']
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_guild_available(self, guild):
        self.get_cog('Roles').register_bot_roles(guild)

    def run_bastion(self):
        # This is built this way so we can mock out Bot.run
        self.run(self.token)


def init_bastion(config):
    bastion = BastionBot(config, discord_commands.when_mentioned,
                         guild_subscriptions=False,
                         fetch_offline_members=False)
    bastion.load_extension('bastion.commands.roles')
    bastion.load_extension('bastion.commands.misc')
    bastion.load_extension('bastion.commands.track')
    return bastion
