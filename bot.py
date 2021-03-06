import discord
import os
from discord.ext import commands
import sentry_sdk
from dotenv import load_dotenv

load_dotenv()
client = commands.Bot(command_prefix="!", description="""Lista de comandos que pueden ser utilzados en este servidor
ten en cuenta que para el uso de algún comando necesitarás tener 
X rol/permiso, si el comando lo necesita este te lo dirá.
Saludos y no me rompas el bot JoseLuis.""")

sentry_sdk.init(
    os.getenv("SENTRY"),
    traces_sample_rate=1.0)


@client.event
async def on_ready():
    print('bot ready')
    await client.change_presence(status=discord.Status.online, activity=discord.Game('Admin this server'))


@client.command()
@commands.has_role("Admin-Bot")
async def load(ctx, extension):
    "Carga de un nuevo fichero de comandos"
    client.load_extension(f'commands.{extension}')


@client.command()
@commands.has_role("Admin-Bot")
async def unload(ctx, extension):
    "Eliminación de un fichero de comandos"
    client.unload_extension(f'commands.{extension}')


@client.command()
@commands.has_role("Admin-Bot")
async def reload(ctx, extension):
    "Actulización de un nuevo fichero de comandos"
    client.unload_extension(f'commands.{extension}')
    client.load_extension(f'commands.{extension}')


for filename in os.listdir('./commands'):
    if filename.endswith('.py'):
        client.load_extension(f'commands.{filename[:-3]}')

client.run(os.getenv("DISCORD_API"))
