from discord.ext import commands
from utils.Functions import is_integer


class MainCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="ping")
    async def ping(self, ctx):
        "Comando de para ver si el bot está en línea"
        await ctx.send("pong!")

    @commands.command(aliases=["purge"])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=40):
        "Borrar mensajes del canal, si no pasas ningún valor, se borrarán 40"
        print(amount)
        if is_integer(amount) and amount == 40:
            await ctx.channel.purge(limit=amount)
        else:
            await ctx.send('```El comando `!clear` debe ir con un número entero. `!clear 5` ```')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send('Welcome {0.mention}.'.format(member))


def setup(client):
    client.add_cog(MainCommands(client))
