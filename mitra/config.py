from typing import Final, List
from environs import Env

env = Env()
env.read_env()

DISCORD_TOKEN: Final[str] = env.str("DISCORD_TOKEN")
COMMAND_PREFIX: Final[str] = env.str("COMMAND_PREFIX", ".")
TEXT_CHANNEL_WHITELIST: Final[List[str]] = env.list(
    "TEXT_CHANNEL_WHITELIST",
    ["oblivious-bot"]
)