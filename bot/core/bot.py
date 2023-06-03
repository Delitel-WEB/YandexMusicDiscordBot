import discord
from discord.ext import commands


class PersistentViewBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all() # Включены все intents события
        super().__init__(intents=intents, command_prefix="$$", help_command=None)

    async def setup_hook(self):
        await self.tree.sync()