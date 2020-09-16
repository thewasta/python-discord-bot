import os
import time

import discord
from discord import FFmpegPCMAudio
from discord.ext import commands


class VoiceCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel is None and after.channel is not None and member.bot == False:
            print("entra")
            try:
                vc = await after.channel.connect()
            except discord.ClientException:
                print("Error conectado el bot al canal de voz")
                pass
            try:
                assets = os.getcwd() + "\\assets"
                print(assets)
                source = FFmpegPCMAudio(source=assets + r'tula5.mp3')
                player = vc.play(source)
            except discord.ClientException:
                print("Error reproduciendo el audio")
                pass
            esta_reproduciendo = vc.is_playing()
            time.sleep(1)
            while esta_reproduciendo == True:
                esta_reproduciendo = vc.is_playing()
            await vc.disconnect()

    @commands.command()
    async def prueba(self, ctx):
        assets = os.getcwd() + "\\assets"
        print(assets)

    @commands.command()
    async def play(self, ctx, url):
        players = []
        guild = ctx.message.guild
        voice_client = guild.voice_client
        player = await voice_client.create_ytdl_player(url)
        players[guild.id] = player
        player.start()

    @commands.command()
    async def join(self, ctx):
        channel = ctx.message.author.voice.channel
        await channel.connect()

    @commands.command()
    async def leave(self, ctx):
        server = ctx.message.guild.voice_client
        await server.disconnect()


def setup(client):
    client.add_cog(VoiceCommands(client))
