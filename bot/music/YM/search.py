from .import client
from yandex_music import Artist as artist, Track as track, Playlist as playlist, Album as album
from .Album import Album
from .Playlist import Playlist
from .Track import Track


async def search(prompt):
    mediaItem = await client.search(prompt)

    if not mediaItem.tracks and not mediaItem.best:
        return None
    else:
        if isinstance(mediaItem.best.result, track):
            return await Track(track_object=mediaItem.best.result).fetch_track()
        elif isinstance(mediaItem.best.result, album):
            return await Album(mediaItem.best.result.id).fetch_album()
        elif isinstance(mediaItem.best.result, artist):
            return await Playlist(mediaItem.playlists.results[0].uid, mediaItem.playlists.results[0].kind).fetch_playlist()
        else:
            return None
        