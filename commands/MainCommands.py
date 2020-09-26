import discord
from discord.ext import commands


class MainCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="ping")
    async def ping(self, ctx):
        "Comando de para ver si el bot está en línea"

        await ctx.send("pong!")

    @commands.command(aliases=["purge"])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int = 40):
        "Borrar mensajes del canal, si no pasas ningún valor, se borrarán 40. Es necesario permisos."
        await ctx.channel.purge(limit=amount)

    @clear.error
    async def clear_error_handler(self, ctx: discord.Message, error):
        await ctx.send('Asegurate de escribir un número separado por espacio junto al comando.\n !help clear')

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send('Welcome {0.mention}.'.format(member))


def setup(client):
    client.add_cog(MainCommands(client))
