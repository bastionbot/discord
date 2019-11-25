from discord import utils, Embed
from discord.ext.commands import Cog, command, group

from bastion.commands.misc import eight_ball, roll_dice, decide, is_art, playlist

class Misc(Cog):
    """
    Miscellaneous fun commands.
    """

    @command(aliases=['8ball'])
    async def eightball(self, ctx, question=None):
        """
        Randomly returns Magic 8-Ball-style answers.
        """
        try:
            answer = eight_ball.get_answer(question)
        except ValueError as error:
            await ctx.send(str(error))
        else:
            await ctx.send(answer)

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
            await ctx.send(f'{result}: **{sum(result)}**')

    @command()
    async def decide(self, ctx, *, options):
        """
        Make the bot decide stuff for you!
        Separate each option with "or", for example:
        `decide pizza or burger`
        """
        try:
            result = decide.decide(options)
        except ValueError as e:
            await ctx.send(str(e))
        else:
            await ctx.send(result)

    @command(aliases=['is', 'Is'])
    async def is_art(self, ctx, art=None):
        """
        Answers the immortal question, "Is this art?"
        """
        await ctx.send(f'**{is_art.is_art(art)}**')
    @command()
    async def playlist(self, ctx):
        await ctx.send(f'Bulding playlist, please wait...')
        await ctx.send(f'{playlist.build_playlist()}')



def setup(bot):
    bot.add_cog(Misc())
