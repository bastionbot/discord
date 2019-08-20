import random
from discord import utils, Embed
from discord.ext.commands import Cog, command, group

class Misc(Cog):
    """
    Miscellaneous fun commands.
    """
    def __init__(self, bot):
        self.bot = bot

    @command()
    async def roll(self, ctx, dice=None):
        """
        Rolls all kinds of dice.
        You can specify how many, and what kind of dice to roll with the format XdY.
        X is how many dice (optional, defaults to 1).
        Y is how many sides each die has.
        For example, `roll 2d6` will roll two six-sided dice.
        `roll d20` will roll a 20-sided die.
        Pass nothing to roll a 6-sided die.
        """
        n_dice = 1
        faces = 6
        if dice:
            n_dice, faces = dice.split('d')
            if not faces:
                await ctx.send('Could not extract number of faces.')
                return
            if not n_dice:
                n_dice = 1
            faces = int(faces)
            n_dice = int(n_dice)
        results = list(map(random.randint, [1] * n_dice, [faces] * n_dice))
        await ctx.send(f'{results}: **{sum(results)}**')

    @command(aliases=['add'])
    async def decide(self, ctx, *, role_name):
        """
        Decide.
        """
        pass


def setup(bot):
    bot.add_cog(Misc(bot))
