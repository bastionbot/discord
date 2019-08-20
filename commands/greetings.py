from discord import Member
from discord.ext.commands import Cog, command, group

class Greetings(Cog):
    """
    Greetings category docstring
    """
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @group()
    async def hello(self, ctx):
        """Says hello"""
        if ctx.invoked_subcommand is not None:
            return
        help_command = self.bot.help_command
        # We inject the command context so the help command can know where
        # to send its reply
        help_command.context = ctx
        await help_command.send_group_help(self.hello)

    @hello.command()
    async def world(self, ctx):
        """Says Hello world! """
        await ctx.send('Hello world!')

    @hello.command()
    async def member(self, ctx, *, member: Member = None):
        """ Says hello to a member or to the member that sent this command"""
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send('Hello {0.name}~'.format(member))
        else:
            await ctx.send('Hello {0.name}... This feels familiar.'.format(member))
        self._last_member = member


def setup(bot):
    bot.add_cog(Greetings(bot))
