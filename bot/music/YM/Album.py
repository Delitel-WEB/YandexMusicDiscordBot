from .import client
from .Track import Track
from typing import List


class Album:
    """Альбом"""


    def __init__(self, album_id) -> None:
        self.album_id = album_id
        self.tracks: List[Track] = []
        self.title: str
        self.preview: str


    async def fetch_album(self):
        album = await client.albums_with_tracks(self.album_id)

        self.title = album.title
        self.preview = "https://" + album.og_image.replace("%%", "1000x1000")

        for track in album.volumes[0]:
            self.tracks.append(await Track(track_object=track).fetch_track())

        return self