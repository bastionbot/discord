import random
from discord import utils, Embed
from discord.ext.commands import Cog, command, group

from bastion.commands.misc import eight_ball, roll_dice

class Misc(Cog):
    """
    Miscellaneous fun commands.
    """

    @command(aliases=['8ball'])
    async def eightball(self, ctx, question=None):
        """
        Randomly returns one of the 20 original answers in a Magic 8-Ball
        """
        try:
            answer = eight_ball.get_answer(question)
        except ValueError as error:
            await ctx.send(str(error))
        else:
            await ctx.send(f'**{answer}**')

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
        try:
            result = roll_dice.roll(dice)
        except ValueError as e:
            await ctx.send(str(e))
        else:
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
