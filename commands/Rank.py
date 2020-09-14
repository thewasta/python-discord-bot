from discord.ext import commands

class LoLRanking(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def rank(self, ctx):
        await ctx.send('add user')


def setup(client):
    client.add_cog(LoLRanking(client))
