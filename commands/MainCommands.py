import discord
from discord.ext import commands
from utils.LoLRankingUtils import is_integer
import sentry_sdk


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
        if is_integer(amount):
            await ctx.channel.purge(limit=amount)
        else:
            await ctx.send('```El comando `!clear` debe ir con un número entero. `!clear 5` ```')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        sentry_sdk.capture_exception(Exception(error))

    @clear.error
    async def clear_error_handler(self, ctx: discord.Message, error):
        sentry_sdk.capture_exception(
            Exception(error, ctx.message.content, ctx.message.author.name + ctx.message.author.discriminator))

    @ping.error
    async def ping_error_handler(self, ctx, error):
        sentry_sdk.capture_exception(Exception(error, ctx.message.author.name + ctx.message.author.discriminator))

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send('Welcome {0.mention}.'.format(member))


def setup(client):
    client.add_cog(MainCommands(client))
