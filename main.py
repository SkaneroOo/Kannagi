from Kannagi import Kannagi
from os import environ

from discord import Intents

from dotenv import load_dotenv
load_dotenv()


intents = Intents.default()
intents.message_content = True

bot = Kannagi(intents=intents, dburl="http://localhost:8000", dbusername="root", dbpassword="root", translations_path="/locals", shard_count=1)

bot.run(environ.get("TOKEN", None))