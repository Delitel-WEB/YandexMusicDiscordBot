from .import Bot
from discord import Interaction, Colour, Embed


@Bot.tree.command(description="Помощь")
async def help(interaction: Interaction):
    commands = await Bot.tree.fetch_commands()
    embed = Embed(
        title="Помощь",
        description="Здесь описаны все существующие команды бота:",
        color=Colour.blurple()
    )
    embed.add_field(
        name="Музыка",
        value=  f"{commands[0].mention} - проигрывание Трека/Альбома/Плейлиста/Подкаста/Книги из Яндекс.Музыки.\n\n"
                "Данный бот проигрывает Треки/Альбомы/Плейлисты/Подкасты/Книги из Яндекс.Музыки" \
                f"Чтобы воспроизвести что либо вы можете отправить ссылку/название трека или отрывок из него этой командой!",
        inline=False
    )

    await interaction.response.send_message(embed=embed, ephemeral=True)