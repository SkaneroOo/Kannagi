from ..logger import Logger
from .ping import Ping
from .character import Character
from .profile import Profile
from .register import Register
from .admin_utils import Admin
from .spawn import Spawn
from Kannagi import Kannagi

logger = Logger(__name__)

async def setup(bot: Kannagi):
    await bot.add_cog(Ping(bot))
    await bot.add_cog(Character(bot))
    await bot.add_cog(Profile(bot))
    await bot.add_cog(Register(bot))
    await bot.add_cog(Admin(bot))
    await bot.add_cog(Spawn(bot))