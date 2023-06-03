from bot.core import Bot
from bot.cfg import token
import bot.interactions
import bot.music


@Bot.event
async def on_ready():
    print("Бот запущен!")

Bot.run(token)
