from discord.ext.commands import Cog
from discord import Interaction, app_commands, Embed

from Kannagi.logger import Logger
from Kannagi import Kannagi

async def character_autocomplete(interaction: Interaction, current: str) -> list[app_commands.Choice[str]]:
    data = await interaction.client.database.execute(f"SELECT id, name FROM characters WHERE name ?~ '{current}' LIMIT 25;")
    return [
        app_commands.Choice(name=char["name"], value=char["id"])
        for char in data
    ]

class Character(Cog):

    def __init__(self, bot: Kannagi):
        self.bot: Kannagi = bot
        self.translate = self.bot.tree.translator.sync_translate
        self.logger = Logger(__name__)
        self.logger.info("Successfully loaded character commands")

    @app_commands.command()
    async def character(self, interaction: Interaction, character_id: int):
        data = await self.bot.database.execute(f"SELECT name, id FROM characters:{character_id};")
        if not data:
            embed = Embed(title=self.translate("char_not_found", interaction.locale))
            embed.color = 0xff0000
            await interaction.response.send_message(embed=embed)
            self.logger.debug(f"Character with id {character_id} not found")
            return
        data = data[0]
        embed = Embed(title=data["name"])
        embed.set_image(url=f"https://kannagicdn.netlify.app/{data['id'].split(':')[1]}_6.png")
        embed.set_footer(text=f"AniList ID: {character_id}")
        embed.color = 0x00ff00
        await interaction.response.send_message(embed=embed)
        self.logger.debug(f"Character {data['name']} found")

    @app_commands.command()
    @app_commands.autocomplete(character=character_autocomplete)
    async def character_name(self, interaction: Interaction, character: str):
        self.logger.debug(character)
        data = await self.bot.database.execute(f"SELECT name, id FROM {character};")
        if not data:
            embed = Embed(title=self.translate("char_not_found", interaction.locale))
            embed.color = 0xff0000
            await interaction.response.send_message(embed=embed)
            self.logger.debug(f"Character with id {character} not found")
            return
        data = data[0]
        embed = Embed(title=data["name"])
        embed.set_image(url=f"https://kannagicdn.netlify.app/{data['id'].split(':')[1]}_6.png")
        embed.set_footer(text=f"AniList ID: {character.split(':')[1]}")
        embed.color = 0x00ff00
        await interaction.response.send_message(embed=embed)
        self.logger.debug(f"Character {data['name']} found")

async def setup(bot: Kannagi):
    await bot.add_cog(Character(bot))