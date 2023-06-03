from typing import List
from .import client
from yandex_music import Track as track_object_
from yandex_music.track_short import TrackShort


class Track:
    """Трек"""


    def __init__(self, album_id: int = None, track_id: int = None, track_object: track_object_ = None) -> None:
        self.album_id = album_id
        self.track_id = track_id
        self.track_object = track_object
        self.title: str
        self.artists: List[str]
        self.preview: str
        self.track_link: str
        self.available: bool


    async def fetch_track(self):
        if self.track_object:
            if isinstance(self.track_object, TrackShort):
                track = self.track_object.track
                self.track_object = self.track_object.track
            else:
                track = self.track_object
        else:
            track = (await client.tracks([f"{self.track_id}:{self.album_id}"]))[0]
            self.track_object = track

        if track.available:
            self.artists = track.artists
            self.title = track.title
            self.preview = "https://" + track.cover_uri.replace("%%", "1000x1000")
            self.track_link = f"https://music.yandex.ru/album/{self.album_id}/track/{self.track_id}"

        self.available = track.available

        return self
        
    
    async def download(self):
        return await self.track_object.download_bytes_async()

