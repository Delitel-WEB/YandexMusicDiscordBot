import re
from .Playlist import Playlist
from .Track import Track
from .Album import Album
from .search import search


async def fetch_link(link: str):
    """Обработка полученной ссылки"""

    valid_url_pattern = r"https://music\.yandex\.ru"
    pattern_playlist = r"/users/([^/]+)/playlists/(\d+)"
    pattern_track = r"/album/(\d+)/track/(\d+)"
    pattern_album = r"/album/(\d+)"
    pattern_text = r"^(https://music\.yandex\.ru)?[^/]*$"

    match_valid_url = re.search(valid_url_pattern, link)
    match_text = re.search(pattern_text, link)
    if not match_valid_url and not match_text:
        return None  # Если ссылка не является допустимой ссылкой на Яндекс.Музыку, возвращаем None

    match_playlist = re.search(pattern_playlist, link)
    match_track = re.search(pattern_track, link)
    match_album = re.search(pattern_album, link)

    if match_playlist:
        user_id = match_playlist.group(1)
        playlist_id = match_playlist.group(2)
        
        return await Playlist(user_id, playlist_id).fetch_playlist()
    elif match_track:
        album_id = match_track.group(1)
        track_id = match_track.group(2)

        return await Track(album_id, track_id).fetch_track()
    elif match_album:
        album_id = match_album.group(1)
        
        return await Album(album_id).fetch_album()
    elif match_text:
        return await search(link)
    else:
        return None