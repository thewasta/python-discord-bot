import discord
from discord.ext import commands
from utils.LoLRankingUtils import player_level, get_profile_details_for_embed, get_player_queue_details_for_embed, \
    get_string_match_embed, currently_in_game

league_graph_url = "https://www.leagueofgraphs.com/match/euw/"


class LeagueOfLegends(commands.Cog):
    def __init__(self, client: discord.Client):
        self.client = client

    @commands.command(name="stats", aliases=["elo", "profile"])
    async def stats_profile(self, ctx, args=None, region=None):
        """Muestra los datos en SOLOQ y FLEXQ de un único perfil.
        Partidas jugadas, champs más jugados y resultado de sus últimas partidas.
        El nombre de usuario debe ser escrito sin espacio, ejemplo: !elosolo tmsthewasta.
        El icono verde junto al título se refiere a si el jugador está en partida o no.
        """
        if args is None:
            await ctx.send('Debes incluir el nombre de invocador sin espacios !elosolo tmsthewasta')
            return
        player_info_level = player_level(args)
        in_game = currently_in_game(args)
        profile_champs_details = get_profile_details_for_embed(args)
        profile_stats_details = get_player_queue_details_for_embed(args)
        last_games = get_string_match_embed(args, 5)
        embed = discord.Embed(
            title="Perfil de {}: Nivel {} {}".format(profile_stats_details[1],
                                                     player_info_level, in_game),
            colour=discord.Colour.dark_green()
        )
        embed.add_field(name="Mejores campeones", value=profile_champs_details, inline=True)
        embed.add_field(name="Estadísticas Clasificatorias", value=profile_stats_details[0],
                        inline=True)
        embed.add_field(name="Últimas partidas", value=last_games, inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def analyze(self, ctx):
        print("analuze")

    @stats_profile.error
    async def stats_error(self, ctx, error):
        await ctx.send('El usuario `{}` no existe'.format(ctx.message.content.split(' ')[1]))

    @commands.command()
    async def testembed(self, ctx):
        embed = discord.Embed(
            title="test",
            colour=discord.Colour.dark_green()
        )
        embed.add_field(name='Aqioe', value="[Text](https://yoururl.com/ 'Text will appear if you hover here')")
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(LeagueOfLegends(client))
