from configparser import ConfigParser

from discord import Client


class BastionBot(Client):

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))

config = ConfigParser()
config.read('config.ini')
bastion = BastionBot()
bastion.run(config["client"]["token"])
