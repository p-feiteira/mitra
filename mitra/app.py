import logging

from mitra import bot
from mitra.config import DISCORD_TOKEN

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)