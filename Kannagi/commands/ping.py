from discord.ext.commands import Cog
from discord import Interaction, app_commands

from Kannagi.logger import Logger
from Kannagi import Kannagi

class Ping(Cog):

    def __init__(self, bot: Kannagi):
        self.bot: Kannagi = bot
        self.logger = Logger(__name__)
        self.logger.info("Successfully loaded ping command")

    @app_commands.command()
    async def ping(self, interaction: Interaction):
        await interaction.response.send_message(f"Pong {int(self.bot.latency*1000)}ms")
        self.logger.info("Pinging")