from dataclasses import dataclass

from environs import Env

@dataclass
class TgBot:
  token: str

@dataclass
class Config:
  tg_bot: TgBot

def load_config(path: str | None = None) -> Config:
  env = Env()
  env.read_env(path)
  return Config(TgBot(env('BOT_TOKEN')))

ADMIN_CHAT_IDS = [535171689]
CHANNEL_ID = -1002299602595
BOT_URL = "https://t.me/playysbot"
CHANNEL_URL = "https://t.me/dfadr32"