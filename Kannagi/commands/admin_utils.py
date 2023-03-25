from discord.ext.commands import Cog
from discord import Interaction, app_commands, Object

from Kannagi.logger import Logger
from Kannagi import Kannagi

class Admin(Cog):

    def __init__(self, bot: Kannagi):
        self.bot: Kannagi = bot
        self.logger = Logger(__name__)
        self.logger.info("Successfully loaded admin utilities")

    @app_commands.command()
    async def reload(self, interaction: Interaction):
        if interaction.user.id != 215553356452724747:
            await interaction.response.send_message("You cannot use that command")
            return
        self.logger.info("Reloading all commands")
        await self.bot.reload_extension("Kannagi.commands")
        await self.bot.tree.sync()
        await interaction.response.send_message("Commands reloaded", ephemeral=True)
        self.logger.info("Reloaded all commands")