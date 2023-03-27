from discord.ext.commands import Cog
from discord import Interaction, app_commands, ui, ButtonStyle, Embed
from datetime import datetime, timezone
from surrealdb import HTTPClient

from Kannagi.logger import Logger
from Kannagi import Kannagi

class CardView(ui.View):
    def __init__(self, bot: Kannagi, card, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_item(CardButton(bot, card, self))
        self.timeout = 300.0


class CardButton(ui.Button):
    def __init__(self, bot: Kannagi, card, view: CardView, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = view
        self.style = ButtonStyle.green
        self.label = "Claim card"
        self.bot = bot
        self.card = card

    async def callback(self, interaction: Interaction):
        data = await self.bot.database.execute(f"SELECT inventory_slots FROM profiles:{interaction.user.id}")
        if not data:
            await interaction.response.send_message(self.bot.tree.translator.sync_translate("user_self_no_profile", interaction.locale), ephemeral=True)
            return
        data = data[0]
        character_count = await self.bot.database.execute(f"select count() from inventory where owner=profiles:{interaction.user.id} group by all")
        if len(character_count) == 0:
            character_count = 0
        else:
            character_count = character_count[0]["count"]
        if character_count >= data["inventory_slots"]:
            await interaction.response.send_message(self.bot.tree.translator.sync_translate("no_inventory_space", interaction.locale), ephemeral=True)
            return
        self.parent.stop()
        await self.bot.database.execute(f"INSERT INTO inventory (card_id, owner) VALUES ({self.card['id']}, profiles:{interaction.user.id}); UPDATE profiles:{interaction.user.id} SET xp += 100;")
        embed = interaction.message.embeds[0]
        embed.title = self.bot.tree.translator.sync_translate("card_claimed", interaction.locale).format(interaction.user.display_name)
        embed.color = 0x00ff00
        await interaction.response.edit_message(embed=embed, view=None)
        # await interaction.response.send_message(self.bot.tree.translator.sync_translate("success_claim", interaction.locale).format(self.card["name"]))


class CardEmbed(Embed):
    def __init__(self, interaction: Interaction, card, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = interaction.client.tree.translator.sync_translate("new_card_spawn_title", interaction.locale)
        self.description = "**" + card["name"] + "**"
        self.set_image(url=card["image"])
        self.color = 0x0000ff
        # self.set_thumbnail(url = interaction.client.user.avatar.url)

class Spawn(Cog):

    def __init__(self, bot: Kannagi):
        self.bot: Kannagi = bot
        self.translate = self.bot.tree.translator.sync_translate
        self.logger = Logger(__name__)
        self.logger.info("Successfully loaded spawn command")

    @app_commands.command()
    async def spawn(self, interaction: Interaction):
        data = await self.bot.database.execute(f"SELECT summon FROM profiles:{interaction.user.id}")
        if not data:
            await interaction.response.send_message(self.translate("user_self_no_profile", interaction.locale), ephemeral=True)
            return
        data = data[0]

        data["summon"] = datetime.fromisoformat(data["summon"])
        now = datetime.now(timezone.utc)
        if data["summon"] > now:
            await interaction.response.send_message(self.translate("cannot_summon_yet", interaction.locale).format(int(data["summon"].timestamp())), ephemeral=True)
            return
        
        await self.bot.database.execute(f"UPDATE profiles:{interaction.user.id} SET summon = time::now() + 5m;")
        card = (await self.bot.database.execute(f"select id, image, name from characters order rand() limit 1;"))[0]
        view = CardView(self.bot, card)
        embed = CardEmbed(interaction, card)
        await interaction.response.send_message(embed=embed, view=view)