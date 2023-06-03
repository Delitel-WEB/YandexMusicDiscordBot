from .import Bot
from discord import Interaction, app_commands, Embed, Colour
from ..music.YM.fetch_link import fetch_link
from ..music.voice import VoiceManager
from ..music import GM
from ..music.YM.Track import Track
from ..music.YM.Album import Album
from ..music.YM.Playlist import Playlist
from ..music.event_loop import event_loop


@Bot.tree.command(description="Проигрывание трека")
@app_commands.describe(track="Название Трека/Плейлиста/Альбома/Подкаста/Книги или ссылка(Яндекс.Музыка)!")
@app_commands.rename(track="трек")
async def play(interaction: Interaction, track: str):
    await interaction.response.send_message("Ожидайте...", ephemeral=True)
    if interaction.user.voice:
        VM: VoiceManager = await GM.get_guild(interaction.user.voice.channel, interaction.channel)
        mediaItem = await fetch_link(track)
        if not mediaItem:
            await interaction.edit_original_response(content="По вашему запросу ничего не найдено!")
        else:
            if not VM.queue:
                VM.queue.append(mediaItem)
                try:
                    await add_to_queue_message(interaction, mediaItem)
                except: ...
                await event_loop(VM)
                await GM.delete_guild(interaction.guild.id)
            else:
                if interaction.user.voice.channel == VM.voiceChannel:
                    VM.queue.append(mediaItem)
                    await add_to_queue_message(interaction, mediaItem)
                else:
                    await interaction.edit_original_response(content="Похоже бот уже где-то играет!")
    else:
        await interaction.edit_original_response(
                content="Для выполнения этого действия вы должны находится в голосовом канале!"
            )


async def add_to_queue_message(interaction: Interaction, mediaItem):
    embed = Embed(
        colour=Colour.green(),
        description="{} `{}` добавлен в очередь!"
    )

    if isinstance(mediaItem, Track):
        embed.description = embed.description.format("Трек", mediaItem.title)
    elif isinstance(mediaItem, Album):
        embed.description = embed.description.format("Албом", mediaItem.title)
    elif isinstance(mediaItem, Playlist):
        embed.description = embed.description.format("Плейлист", mediaItem.title)

    await interaction.edit_original_response(embed=embed)
