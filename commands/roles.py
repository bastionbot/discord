from discord import utils, Embed
from discord.ext.commands import Cog, command, group

class Roles(Cog):
    """
    Commands related to user self-servicing roles.
    """
    def __init__(self, bot):
        self.bot = bot
        self.bot_role_map = {}

    def register_bot_roles(self, guild):
        bot_guild_user = utils.find(lambda member: member.id == self.bot.user.id, guild.members)
        # I'm pretty sure @everyone is always the first role
        bot_roles = bot_guild_user.roles[1:]
        self.bot_role_map[guild.id] = [role.id for role in bot_roles]

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
        roles = self._get_available_roles(ctx.guild)
        roles.reverse()

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

    @role.command(aliases=['add'])
    async def join(self, ctx, *, role_name):
        """
        Joins a role.
        """
        role = utils.get(ctx.guild.roles, name=role_name)
        if not role:
            await ctx.send('Role not found.')
            return

        available_roles = self._get_available_roles(ctx.guild)
        if role not in available_roles:
            await ctx.send('I cannot give out roles higher than my own.')
            return

        await ctx.author.add_roles(role)
        await ctx.send('Succesfully added role.')

    @role.command(aliases=['remove'])
    async def leave(self, ctx, *, role_name):
        """
        Leaves a role
        """
        role = utils.get(ctx.guild.roles, name=role_name)
        if not role:
            await ctx.send('Role not found.')
            return

        available_roles = self._get_available_roles(ctx.guild)
        if role not in available_roles:
            await ctx.send('I cannot take out roles higher than my own.')
            return

        await ctx.author.remove_roles(role)
        await ctx.send('Succesfully removed role.')

    def _get_available_roles(self, guild):
        """
        Gets the roles that the bot can add to the other users
        """
        roles = []
        bot_roles_ids = self.bot_role_map[guild.id]
        # We skip the first role, as it is @everyone
        for role in guild.roles[1:]:
            # We break out on the first role that the bot has, just to be safe
            if role.id in bot_roles_ids:
                break
            roles.append(role)
        return roles



def setup(bot):
    bot.add_cog(Roles(bot))
