from discord import Member
from discord.ext.commands import Cog, command, group

class Greetings(Cog, name='greetings'):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @group()
    async def hello(self, ctx):
        """Says hello"""
        if ctx.invoked_subcommand is None:
            await ctx.send('Command not found.')

    @hello.command()
    async def world(self, ctx):
        await ctx.send('world!')

    @hello.command()
    async def member(self, ctx, *, member: Member = None):
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send('Hello {0.name}~'.format(member))
        else:
            await ctx.send('Hello {0.name}... This feels familiar.'.format(member))
        self._last_member = member


def setup(bot):
    bot.add_cog(Greetings(bot))
