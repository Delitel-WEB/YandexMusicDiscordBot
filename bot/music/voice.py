from .YM.Track import Track
from discord import Message, VoiceChannel, VoiceClient, TextChannel


class VoiceManager:
    

    def __init__(self, voiceChannel: VoiceChannel, textChannel: TextChannel):
        self.voiceChannel: VoiceChannel = voiceChannel
        self.textChannel: TextChannel = textChannel
        self.voiceClient: VoiceClient = None
        self.message: Message = None
        self.counter: int = 0
        self.queue: list = []


    async def connect(self):
        """Подключение к голосовому чату"""
        self.voiceClient = await self.voiceChannel.connect()


    async def disconnect(self):
        """Отключение от голосового чата""" 
        await self.voiceClient.disconnect()


    async def first_track(self):
        if isinstance(self.queue[0], Track):
            return self.queue[0]
        else:
            return self.queue[0].tracks[0]


    async def skip(self, playlist=False):
        if not playlist:
            if isinstance(self.queue[0], Track):
                del self.queue[0]
            else:
                if len(self.queue[0].tracks) > 0:
                    del self.queue[0].tracks[0]
                else:
                    del self.queue[0]
        else:
            del self.queue[0]


    async def delete_message(self):
        try:
            await self.message.delete()
        except: ...

    
    async def play(self): ...


class GuildsManager:
    guilds: dict = {}


    async def get_guild(self, voiceChannel: VoiceChannel, textChannel: TextChannel):
        guild_id = voiceChannel.guild.id

        if guild_id in self.guilds:
            return self.guilds[guild_id]
        else:
            VM = VoiceManager(voiceChannel, textChannel)
            await self.add_guild(guild_id, VM)
            return VM


    async def add_guild(self, guild_id: int, VM: VoiceManager):
        if guild_id not in self.guilds:
            self.guilds[guild_id] = VM


    async def delete_guild(self, guild_id: int):
        if guild_id in self.guilds:
            del self.guilds[guild_id]

