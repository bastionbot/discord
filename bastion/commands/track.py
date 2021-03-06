from datetime import datetime
import asyncio

from discord.ext.commands import Cog, command, group

from bastion.utils.trackers.parsers.gofundme import gofundme
from bastion.utils.trackers import Timer


class Track(Cog):

    DEFAULT_TIMEOUT = 60 * 60 * 12 # 12 hours

    def __init__(self, bot):
        self.bot = bot
        self.timers = {}

    @group()
    async def track(self, ctx):
        """
        Gofundme tracking commands
        """
        if ctx.invoked_subcommand is not None:
            return
        await ctx.send(f'Command not found. Type `!help track or @{self.bot.user} help track` for a list of commands.')

    @track.command()
    async def stop(self, ctx, name):
        """
        Stops an active tracking by name.
        See the list command for a list of currently active tracking.
        """
        thread = self.timers.get(name)
        if thread:
            thread.cancel()
            del self.timers[name]
            await ctx.send(f'Tracking of {name} stopped successfully.')
            return
        await ctx.send(
            f'Tracking by the name of {name} not found. Did you spell the name correctly? '
            f'Type `!track list or @{self.bot.user} track list` for a list of active trackings.'
        )

    @track.command()
    async def list(self, ctx):
        """
        List currently tracked gofundmes.
        """
        if not list(self.timers.keys()):
            await ctx.send("'I'm not currently tracking any GoFundMe pages.'")
            return
        threads = '\n'.join([
            f'{i}) {name}' for i, name in enumerate(self.timers.keys(), 1)
        ])
        await ctx.send(f"I'm currently tracking the following GoFundMe pages!\n>>> {threads}")

    @track.command()
    async def start(self, ctx, url, timeout=DEFAULT_TIMEOUT):
        """
        Give the bot a URL to track a gofundme!
        E.g. @Bastion track start https://www.gofundme.com/f/help-ben-finish-college
        Bastion will keep tabs on the latest contributors and announce progress milestones.
        """
        if not url.split(' ')[-1].startswith('https://www.gofundme.com/f/'):
            await ctx.send(f'<{url}> is not a valid GoFundMe page')
            return
        name = url.split('/')[-1]
        timer = Timer(timeout, gofundme, name, url, ctx)
        self.timers[name] = timer
        await ctx.send(f'Started tracking {name}')
        await timer.run()


def setup(bot):
    bot.add_cog(Track(bot))
