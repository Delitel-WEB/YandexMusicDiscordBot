from .import client
from .Track import Track
from typing import List


class Playlist:
    """Плейлист"""


    def __init__(self, user_id: str, playlist_id: int) -> None:
        self.user_id = user_id
        self.playlist_id = playlist_id
        self.tracks: List[Track] = []
        self.title: str
        self.preview: str

    
    async def fetch_playlist(self):
        playlist = await client.users_playlists(kind=self.playlist_id, user_id=self.user_id)

        self.title = self.user_id if not playlist.title else playlist.title
        self.preview = "https://" + playlist.og_image.replace("%%", "1000x1000")
        
        for track in playlist.tracks:
            self.tracks.append(await Track(track_object=track).fetch_track())

        return self