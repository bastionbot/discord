from configparser import ConfigParser

from discord.ext.commands import Bot, command


class BastionBot(Bot):

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

def main():
    config = ConfigParser()
    config.read('config.ini')
    bastion = BastionBot('!')

    @bastion.command()
    async def hello(ctx, arg):
        await ctx.send(arg)

    # bastion.load_extension('commands.greetings')

    bastion.run(config["client"]["token"])


if __name__ == '__main__':
    main()
