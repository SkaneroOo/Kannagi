from ..logger import Logger
from .ping import Ping
from .character import Character
from Kannagi import Kannagi

logger = Logger(__name__)

async def setup(bot: Kannagi):
    await bot.add_cog(Ping(bot))
    await bot.add_cog(Character(bot))