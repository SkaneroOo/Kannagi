from discord import Intents, Object
from discord.ext.commands import AutoShardedBot
from surrealdb import HTTPClient

from .translator import Translator
from .logger import Logger, LogLevel

GUILD = Object(id=798889494249209907)

class Kannagi(AutoShardedBot):

    def __init__(self, intents: Intents, dburl: str, dbusername: str, dbpassword: str, translations_path: str | None = None, *args, **kwargs):
        super().__init__(intents=intents, command_prefix="->", *args, **kwargs)
        self.logger = Logger(__name__, LogLevel.INFO)
        self.logger.info('Successfully initialised logger')
        self.database = HTTPClient(dburl, username=dbusername, password=dbpassword, namespace="Kannagi", database="KannagiDB")

        self.translations_path = translations_path

        # self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.set_translator(Translator(self.translations_path))
        await self.load_extension("Kannagi.commands")
        self.tree.copy_global_to(guild=GUILD)
        data = await self.database.execute("INFO FOR DB;")
        if data:
            self.logger.info("Successfully connected to database")
        self.logger.info("Successfully initialised translator")
        await self.tree.sync()
        