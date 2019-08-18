from configparser import ConfigParser

from discord.ext.commands import Bot, command, when_mentioned


class BastionBot(Bot):

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

def main():
    config = ConfigParser()
    config.read('config.ini')
    bastion = BastionBot(when_mentioned)

    bastion.load_extension('commands.greetings')

    bastion.run(config["client"]["token"])


if __name__ == '__main__':
    main()
