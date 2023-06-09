from discord import Intents, Object
from discord.ext.commands import AutoShardedBot
from surrealdb import HTTPClient
from os import listdir

from .translator import Translator
from .logger import Logger, LogLevel
from .Database import Database

GUILD = Object(id=798889494249209907)

class Kannagi(AutoShardedBot):

    def __init__(self, intents: Intents, dburl: str, dbusername: str, dbpassword: str, translations_path: str | None = None, *args, **kwargs):
        super().__init__(intents=intents, command_prefix="->", *args, **kwargs)
        self.logger = Logger(__name__, LogLevel.INFO)
        self.logger.info('Successfully initialised logger')
        self.database = Database(dburl, dbusername, dbpassword)

        self.translations_path = translations_path

        # self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.set_translator(Translator(self.translations_path))
        for file in listdir("./Kannagi/commands"):
            if file.endswith(".py"):
                await self.load_extension(f"Kannagi.commands.{file[:file.index('.')]}")
        self.tree.copy_global_to(guild=GUILD)
        data = await self.database.execute("INFO FOR DB;")
        if data:
            self.logger.info("Successfully connected to database")
        self.logger.info("Successfully initialised translator")
        await self.tree.sync()
        