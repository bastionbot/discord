from discord.ext import commands as discord_commands
from discord.ext.commands import Bot
from discord import Activity, ActivityType


class BastionBot(Bot):

    def __init__(self, config, *args, **kwargs):
        self.token = config['client']['token']
        self.config = config
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        thing = Activity(name="@{0} help or !help".format(self.user), state="Extremely Online", type=ActivityType.playing)
        await self.change_presence(activity=thing)

    async def on_guild_available(self, guild):
        self.get_cog('Roles').register_bot_roles(guild)

    def run(self):
        super().run(self.token)


def init_bastion(config):
    bastion = BastionBot(config, discord_commands.when_mentioned_or('!'),
                         guild_subscriptions=False,
                         fetch_offline_members=False)
    bastion.load_extension('bastion.commands.roles')
    bastion.load_extension('bastion.commands.misc')
    bastion.load_extension('bastion.commands.track')
    return bastion
