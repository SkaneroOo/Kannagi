from discord.ext.commands import Cog
from discord import Interaction, app_commands, Member, Embed
from datetime import datetime, timezone

from Kannagi.logger import Logger
from Kannagi import Kannagi

class Profile(Cog):

    def __init__(self, bot: Kannagi):
        self.bot: Kannagi = bot
        self.translate = self.bot.tree.translator.sync_translate
        self.logger = Logger(__name__)
        self.logger.info("Successfully loaded profile command")
        self.ctx_menu = app_commands.ContextMenu(
            name='profile',
            callback=self.menu_profile,
        )
        self.bot.tree.add_command(self.ctx_menu)
        
    async def cog_unload(self) -> None:
        self.bot.tree.remove_command(self.ctx_menu.name, type=self.ctx_menu.type)

    @app_commands.command(name="profile", description="profile_description")
    async def profile(self, interaction: Interaction, user: Member | None = None):
        if not user:
            user = interaction.user
        data = await self.bot.database.execute(f"SELECT * FROM profiles:{user.id} FETCH fav")
        if not data:
            message = self.translate("user_no_profile", interaction.locale)
            if user == interaction.user:
                message = self.translate("user_self_no_profile", interaction.locale)
            await interaction.response.send_message(message, ephemeral=True)
            return
        data = data[0]
        data["daily"] = datetime.fromisoformat(data["daily"])
        embed = Embed(title=self.translate("profile_title", interaction.locale).format(user.display_name))
        embed.set_thumbnail(url=user.avatar.url)
        embed.add_field(name=self.translate("profile_balance", interaction.locale), value=data["balance"])
        level, xp = self.calculate_level(data["xp"])
        embed.add_field(name=self.translate("profile_level", interaction.locale), value=level)
        embed.add_field(name=self.translate("profile_xp", interaction.locale), value=xp)
        if data["daily"] < datetime.now(timezone.utc):
            embed.add_field(name=self.translate("profile_daily_time", interaction.locale), value=self.translate("profile_daily_ready", interaction.locale))
        else:
            embed.add_field(name=self.translate("profile_daily_time", interaction.locale), value=f"<t:{int(data['daily'].timestamp())}:R>")
        embed.color = data["color"]
        if data["fav"]:
            embed.add_field(name=self.translate("profile_fav", interaction.locale), value=data["fav"]["name"], inline=False)
            embed.set_image(url=f"http://kannagi.rf.gd/cards/{data['fav']['id'].split(':')[1]}_6.png")
        await interaction.response.send_message(embed=embed)

    async def menu_profile(self, interaction: Interaction, user: Member):
        data = await self.bot.database.execute(f"SELECT * FROM profiles:{user.id} FETCH fav")
        if not data:
            message = self.translate("user_no_profile", interaction.locale)
            if user == interaction.user:
                message = self.translate("user_self_no_profile", interaction.locale)
            await interaction.response.send_message(message, ephemeral=True)
            return
        data = data[0]
        data["daily"] = datetime.fromisoformat(data["daily"])
        embed = Embed(title=self.translate("profile_title", interaction.locale).format(user.display_name))
        embed.set_thumbnail(url=user.avatar.url)
        embed.add_field(name=self.translate("profile_balance", interaction.locale), value=data["balance"])
        level, xp = self.calculate_level(data["xp"])
        embed.add_field(name=self.translate("profile_level", interaction.locale), value=level)
        embed.add_field(name=self.translate("profile_xp", interaction.locale), value=xp)
        if data["daily"] < datetime.now(timezone.utc):
            embed.add_field(name=self.translate("profile_daily_time", interaction.locale), value=self.translate("profile_daily_ready", interaction.locale))
        else:
            embed.add_field(name=self.translate("profile_daily_time", interaction.locale), value=f"<t:{int(data['daily'].timestamp())}:R>")
        embed.color = data["color"]
        if data["fav"]:
            embed.add_field(name=self.translate("profile_fav", interaction.locale), value=data["fav"]["name"], inline=False)
            embed.set_image(url=f"http://kannagi.rf.gd/cards/{data['fav']['id'].split(':')[1]}_6.png")
        await interaction.response.send_message(embed=embed)

    def calculate_level(self, xp: int) -> tuple[int, int]:
        return 1, 0 #TODO

        
async def setup(bot: Kannagi):
    await bot.add_cog(Profile(bot))