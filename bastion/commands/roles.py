from bastion.utils.role_manager import RoleManager

from discord import utils, Embed, role
from discord.ext.commands import Cog, command, group


class Roles(Cog):
    """
    Commands related to user self-servicing roles.
    """
    def __init__(self, bot):
        self.bot = bot
        self.role_manager = RoleManager()

    def register_bot_roles(self, guild):
        self.role_manager.register_bot_roles(self.bot, guild)

    @group()
    async def role(self, ctx):
        """
        Roles commands
        """
        if ctx.invoked_subcommand is not None:
            return
        await ctx.send(f'Command not found. Type `@{self.bot.user} help role` for a list of commands.')

    @role.command()
    async def list(self, ctx):
        """
        Lists joinable roles.
        Roles higher up in the list have priority when overriding colors.
        """
        roles = reversed(self.role_manager.get_available_roles(ctx.guild))
        if not roles:
            await ctx.send('Could not find any roles! Check if my lowermost role is correctly positioned.')
            return

        # We will probably have to paginate this later
        embed = Embed.from_dict({
            'author': {
                'name': ctx.guild.name,
                'icon_url': str(ctx.guild.icon_url),
            },
            'description': 'Reminder: Roles higher on the list will have priority on your color.',
            'color': 0x40FEF3,
            'fields': [{
                'name': 'Roles',
                'value': '\n'.join([role.name for role in roles]),
            }],
        })

        await ctx.send(embed=embed)


    async def _manage_user_role(self, ctx, role_name, add_role=True):
        present_verb = 'give' if add_role else 'remove'
        past_verb = 'given' if add_role else 'removed'
        preposition = 'to' if add_role else 'from'

        action = ctx.author.add_roles if add_role else ctx.author.remove_roles

        role = utils.get(ctx.guild.roles, name=role_name)
        if not role:
            await ctx.send('Role not found.')
            return

        available_roles = self.role_manager.get_available_roles(ctx.guild)
        if role not in available_roles:
            await ctx.send(f'I cannot {present_verb} roles higher than my own.')
            return

        await action(role)
        await ctx.send(f'Succesfully {past_verb} {role.name} {preposition} {ctx.author.nick if ctx.author.nick else ctx.author.name}.')


    @role.command(aliases=['add'])
    async def join(self, ctx, *, role_name):
        """
        Joins a role.
        """
        await self._manage_user_role(ctx, role_name, add_role=True)


    @role.command(aliases=['remove'])
    async def leave(self, ctx, *, role_name):
        """
        Leaves a role
        """
        await self._manage_user_role(ctx, role_name, add_role=False)


def setup(bot):
    bot.add_cog(Roles(bot))
