import discord
import os
from discord.ext import commands

client = commands.Bot(command_prefix="!")


@client.command()
async def load(ctx, extension):
    client.load_extension(f'commands.{extension}')


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'commands.{extension}')


@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'commands.{extension}')
    client.load_extension(f'commands.{extension}')


for filename in os.listdir('./commands'):
    if filename.endswith('.py'):
        client.load_extension(f'commands.{filename[:-3]}')

client.run("DISCORD_API")
