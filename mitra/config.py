from typing import Final
from environs import Env

env = Env()
env.read_env()

DISCORD_TOKEN: Final[str] = env.str("DISCORD_TOKEN")