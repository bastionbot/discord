import random
from discord import utils, Embed
from discord.ext.commands import Cog, command, group

class Misc(Cog):
    """
    Miscellaneous fun commands.
    """

    @command()
    async def roll(self, ctx, dice=None):
        """
        Rolls all kinds of dice.
        You can specify how many, and what kind of dice to roll with the format XdY.
        X is how many dice (optional, defaults to 1).
        Y is how many sides each die has.
        For example:
        `roll 2d6` will roll two six-sided dice;
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

    @command()
    async def decide(self, ctx, *, options):
        """
        Make the bot decide stuff for you!
        Separate each option with "or", or end your message with y/n for a "yes", "no" pick.
        For example:
        `decide pizza or burger`
        `decide do I go y/n`
        """
        # We probably need to put in more fun messages but meh for now.
        if options.endswith('y/n'):
            await ctx.send(f'**{random.choice(["Yes!", "No!"])}**')
            return
        choices = options.split(" or ")
        if len(choices) == 1:
            await ctx.send('I need to have at least two options!')
            return
        await ctx.send(f'**{random.choice(choices)}**')


def setup(bot):
    bot.add_cog(Misc())
