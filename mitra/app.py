import logging

from mitra.bot import run
from mitra.config import DISCORD_TOKEN

LOG_FORMAT = '[%(levelname)s] %(asctime)s %(name)s: %(message)s'
LOG_LEVEL = logging.INFO

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(LOG_FORMAT))

logging.basicConfig(
    format=LOG_FORMAT,
    handlers=[handler],
    level=LOG_LEVEL
)

if __name__ == "__main__":
    run(DISCORD_TOKEN)
