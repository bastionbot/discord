import logging
from configparser import ConfigParser

from discord.ext import commands
from discord.ext.commands import Bot


class BastionBot(Bot):

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_guild_available(self, guild):
        self.get_cog('Roles').register_bot_roles(guild)


def main():
    # logging.basicConfig(level=logging.INFO)
    config = ConfigParser()
    config.read('config.ini')
    bastion = BastionBot(commands.when_mentioned,
                         guild_subscriptions=False,
                         fetch_offline_members=False)
    bastion.load_extension('commands.roles')
    bastion.load_extension('commands.misc')

    bastion.run(config['client']['token'])

if __name__ == '__main__':
    main()
