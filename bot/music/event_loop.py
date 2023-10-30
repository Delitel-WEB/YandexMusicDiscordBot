import asyncio
from time import time
from io import BytesIO
from ..core import Bot
from .voice import VoiceManager
from discord import TextChannel, Embed, Colour, FFmpegOpusAudio
from ..music.YM.Track import Track
from discord.errors import ClientException
from pydub import AudioSegment
from ..ui.views import MediaPlayer
from ..utils.log import LOGGER

log = LOGGER("event_loop")


async def event_loop(voiceManager: VoiceManager):
    lastActivity = None
    voiceManager.counter = 0 # Счётчик интераций цикла

    if not voiceManager.voiceClient or not voiceManager.voiceClient.is_connected():
        try:
            await voiceManager.connect()
        except ClientException:
            Bot.loop.create_task(error_message(voiceManager.textChannel, disconnectError=True))
    
    if voiceManager.voiceClient:

        while True:
            try:
                voiceManager.counter += 1

                if Bot.user not in voiceManager.voiceChannel.members:
                    voiceManager.voiceClient.stop()
                    await voiceManager.disconnect()
                    await voiceManager.delete_message()
                    Bot.loop.create_task(disconnected_message(voiceManager.textChannel))
                    break
                elif Bot.user in voiceManager.voiceChannel.members and len(voiceManager.voiceChannel.members) == 1:
                    if not lastActivity:
                        lastActivity = time()
                    else:
                        if time() - lastActivity >= 180:
                            await voiceManager.delete_message()
                            voiceManager.voiceClient.stop()
                            await voiceManager.disconnect()
                            Bot.loop.create_task(disconnected_message(voiceManager.textChannel, activity=True))
                            break
                else:
                    lastActivity = None

                if not voiceManager.voiceClient.is_playing() and not voiceManager.voiceClient.is_paused():
                    if not voiceManager.queue:
                        await voiceManager.delete_message()
                        await voiceManager.disconnect()
                        Bot.loop.create_task(disconnected_message(voiceManager.textChannel, notTracks=True))
                        break
                    else:
                        if voiceManager.counter != 1:
                            await voiceManager.skip()
                            
                        try:
                            track = await voiceManager.first_track()
                        except IndexError: continue

                        if not track.available: continue
                        else:
                            trackSource = await track.download()
                        
                        audio_data = AudioSegment.from_file(BytesIO(trackSource), format='mp3')
                        normalized_audio = audio_data.normalize()

                        voiceManager.voiceClient.play(FFmpegOpusAudio(normalized_audio.export(format='wav'), pipe=True, executable="ffmpeg.exe"))у
                        await now_playing(voiceManager, track)
            except Exception as err:
                log.error(err, exc_info=True)
                await error_message(voiceManager.textChannel, unexpected=True)
                break
                    
            await asyncio.sleep(.3)

        await voiceManager.delete_message()
    

async def now_playing(voiceManager: VoiceManager, track: Track):
    await voiceManager.delete_message()

    embed = Embed(
        title="Сейчас Играет",
        description=f"[{track.title}]({track.track_link})"
    )
    artists = [artist.name for artist in track.artists]
    if artists:
        artist_cover_uri = ("https://" + track.artists[0].cover.uri).replace("%%", "300x300")
        artist_uri = f"https://music.yandex.ru/artist/{track.artists[0].id}"

        embed.set_author(name=', '.join(artists), icon_url=artist_cover_uri, url=artist_uri)
    embed.set_thumbnail(url=track.preview)

    voiceManager.message = await voiceManager.textChannel.send(embed=embed, view=MediaPlayer())


async def disconnected_message(channel: TextChannel, activity=False, notTracks=False):
    """Сообщение о отключении от голосового чата!"""

    embed = Embed(
        title="Бот отключен от голосового чата!"    
    )

    if activity:
        embed.description = "Бот отключен из-за отсутствия активности!"
        embed.color=Colour.red()
    elif notTracks:
        embed.description = "Очередь треков окончена!"
        embed.color=Colour.brand_red()
    else:
        embed.color=Colour.red()

    message = await channel.send(embed=embed)
    await asyncio.sleep(10 if activity else 3)
    await message.delete()


async def error_message(channel: TextChannel, disconnectError = False, unexpected=False):
    embed = Embed(
        title="Ошибка!",
        colour=Colour.red()
    )

    if disconnectError:
        embed.description = "Похоже вы отключили бота не самым лучшим способом. Подождите немного..."
    elif unexpected:
        embed.description = "Непредвиденная ошибка!"

    message = await channel.send(embed=embed)
    await asyncio.sleep(10)
    await message.delete()
