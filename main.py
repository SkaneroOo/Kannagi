from Kannagi import Kannagi

from discord import Intents, Interaction

from dotenv import load_dotenv
load_dotenv()
from os import environ


intents = Intents.default()
intents.message_content = True

bot = Kannagi(intents=intents, dburl="http://localhost:8000", dbusername="root", dbpassword="root", translations_path="/locals", shard_count=1)

try:
    bot.run(environ.get("TOKEN", None))
except:
    pass