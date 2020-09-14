import discord
from discord.ext import commands


class MainCommands(commands.Cog, name="Comandos principales"):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(activity=discord.Game('Watching this server'))
        print('bot online')

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('pong')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send('Welcome {0.mention}.'.format(member))


def setup(client):
    client.add_cog(MainCommands(client))
