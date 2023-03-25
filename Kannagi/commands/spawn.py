from discord.ext.commands import Cog
from discord import Interaction, app_commands

from Kannagi.logger import Logger
from Kannagi import Kannagi

class Spawn(Cog):

    def __init__(self, bot: Kannagi):
        self.bot: Kannagi = bot
        self.translate = self.bot.tree.translator.sync_translate
        self.logger = Logger(__name__)
        self.logger.info("Successfully loaded spawn command")

    @app_commands.command()
    async def spawn(self, interaction: Interaction):
        await interaction.response.send_message(f"Pong {int(self.bot.latency*1000)}ms")
        self.logger.info("Pinging")