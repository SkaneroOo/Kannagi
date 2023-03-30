from discord.ext.commands import Cog
from discord import Interaction, app_commands

from Kannagi.logger import Logger
from Kannagi import Kannagi
from datetime import datetime, timezone, timedelta

class Register(Cog):

    def __init__(self, bot: Kannagi):
        self.bot: Kannagi = bot
        self.translate = self.bot.tree.translator.sync_translate
        self.logger = Logger(__name__)
        self.logger.info("Successfully loaded register command")

    @app_commands.command()
    async def register(self, interaction: Interaction):
        data = self.bot.database.execute(f"SELECT * FROM profiles WHERE id={interaction.user.id}")
        if data:
            await interaction.response.send_message(self.translate("register_profile_exist", interaction.locale), ephemeral=True)
            return
        spawn = datetime.now(timezone.utc)-timedelta(minutes=5)
        spawn.microsecond=0
        daily = datetime.now(timezone.utc)
        daily.hour = 0
        daily.minute = 0
        daily.second = 0
        daily.microsecond = 0
        self.bot.database.execute(f"INSERT INTO profiles (id, balance, xp, fav, color, inventory_slots, spawn, daily) VALUES ({interaction.user.id}, 0, 0, null, 6710886, 25, {spawn.isoformat()}, {daily.isoformat()});")
        await interaction.response.send_message(self.translate("register_success", interaction.locale))


async def setup(bot: Kannagi):
    await bot.add_cog(Register(bot))