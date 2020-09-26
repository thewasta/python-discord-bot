from discord.ext import commands
from discord import Message
import sentry_sdk


class CommandErrorHandler(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.content.startswith('!'):
            await Message.delete(message)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """Evento ejecutado cuando hay un error en cualquier comando"""
        sentry_sdk.set_user(value={"user": ctx.message.author.name + ":" + ctx.message.author.discriminator})
        sentry_sdk.capture_exception(Exception(error))


def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
