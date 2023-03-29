from Kannagi import Kannagi
from os import environ

from discord import Intents

from dotenv import load_dotenv
load_dotenv()


intents = Intents.default()
intents.message_content = True

bot = Kannagi(intents=intents, shard_count=1, translations_path="/locals", dburl=environ.get("DBURL", None), dbusername=environ.get("DBUSER", None), dbpassword=environ.get("DBPASS", None))

bot.run(environ.get("TOKEN", None))