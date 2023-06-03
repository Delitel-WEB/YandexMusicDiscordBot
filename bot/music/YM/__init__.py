from yandex_music import ClientAsync
from ...cfg import YMToken
import asyncio

client = asyncio.run(ClientAsync(YMToken).init())
client.request.set_timeout(30)
