from discord.ext.commands import Cog
from discord import Interaction, app_commands

from Kannagi.logger import Logger
from Kannagi import Kannagi

class Register(Cog):

    def __init__(self, bot: Kannagi):
        self.bot: Kannagi = bot
        self.translate = self.bot.tree.translator.sync_translate
        self.logger = Logger(__name__)
        self.logger.info("Successfully loaded register command")

    @app_commands.command()
    async def register(self, interaction: Interaction):
        data = await self.bot.database.execute(f"SELECT * FROM profiles:{interaction.user.id}")
        if data:
            await interaction.response.send_message(self.translate("register_profile_exist", interaction.locale), ephemeral=True)
            return
        await self.bot.database.execute(f"INSERT INTO profiles (id, balance, xp, fav, color) VALUES ({interaction.user.id}, 0, 0, null, 6710886);")
        await interaction.response.send_message(self.translate("register_success", interaction.locale))