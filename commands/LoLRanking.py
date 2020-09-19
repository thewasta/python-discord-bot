import discord
from discord.ext import commands
from utils.LoLRankingUtils import player_level, get_profile_details_for_embed, get_player_queue_details_for_embed, \
    get_string_match_embed

league_graph_url = "https://www.leagueofgraphs.com/match/euw/"


class LoLRanking(commands.Cog):
    def __init__(self, client: discord.Client):
        self.client = client

    @commands.command()
    async def adduserlol(self, ctx, args=None, nick_in_server=None):
        """Añade el usuario al `Rank` para tener trackeado su perfil.
         El usuario debe ser escrito sin espacio, ejemplo `!adduser tmsthewasta`
        """
        if args is None:
            await ctx.send('Debes incluir el nombre de invocador sin espacios !adduserlol tmsthewasta')
            return
        username = args

    @commands.command()
    async def removeuserlol(self, ctx, args=None):
        """Elimina el usuario del `Rank`"""
        if args is None:
            await ctx.send('Debes incluir el nombre de invocador sin espacios !removeuserlol tmsthewasta')
            return
        username = ctx.content.split(" ")[1]

    # RANK DE TODOS
    @commands.command()
    async def ranklol(self, ctx, args=None):
        """
        Ranking de todos los usuarios añadidos, comando: !adduserlol help, para saber más.
        """
        print('a')

    @commands.command(name="stats", aliases=["elo", "profile"])
    async def stats_profile(self, ctx, args=None, region=None):
        """Muestra los datos en SOLOQ y FLEXQ de un único perfil.
        Partidas jugadas, champs más jugados y resultado de sus últimas partidas.
        El nombre de usuario debe ser escrito sin espacio, ejemplo: !elosolo tmsthewasta.
        Por defecto está para EUW, si quiere cambiar el servidor,
        escríbelo separado de un espacio, ejemplo: `!elosolo tmsthewasta na`
        """
        if args is None:
            await ctx.send('Debes incluir el nombre de invocador sin espacios !elosolo tmsthewasta')
            return
        player_info_level = player_level(args)
        profile_champs_details = get_profile_details_for_embed(args)
        profile_stats_details = get_player_queue_details_for_embed(args)
        last_games = get_string_match_embed(args, 5)
        print(last_games)
        embed = discord.Embed(
            title="Perfil de {}: Nivel {} ".format(profile_stats_details[1], player_info_level),
            colour=discord.Colour.dark_green()
        )
        embed.add_field(name="Mejores campeones", value=profile_champs_details, inline=True)
        embed.add_field(name="Estadísticas Clasificatorias", value=profile_stats_details[0],
                        inline=True)
        embed.add_field(name="Últimas partidas", value=last_games, inline=False)
        print('send message')
        await ctx.send(embed=embed)

    @commands.command(name="eloflex", aliases=["flexq"])
    async def elo_flex(self, ctx, args=None):
        """Muestra los datos en FLEXQ de un único perfil.
            Partidas jugadas, champs más jugados y resultado de sus últimas partidas.
            El nombre de usuario debe ser escrito sin espacio, ejemplo: !elosolo tmsthewasta.
            Por defecto está para EUW, si quiere cambiar el servidor,
            escríbelo separado de un espacio, ejemplo: !elosolo tmsthewasta na
            """
        print('a')

    @commands.command()
    async def testembed(self, ctx):
        embed = discord.Embed(
            title="test",
            colour=discord.Colour.dark_green()
        )
        embed.add_field(name='Aqioe', value="[Text](https://yoururl.com/ 'Text will appear if you hover here')")
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(LoLRanking(client))
