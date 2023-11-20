from yandex_music import Client
import random
import enum


@enum.unique
class PlaylistIDs(enum.Enum):
    angry = '1006'
    disgust = '1007'
    fear = '1003'
    happy = '1002'
    sad = '1004'
    surprise = '1005'


def convert_to_id(folder):
    if folder == 'angry':
        return PlaylistIDs.angry.value
    elif folder == 'disgust':
        return PlaylistIDs.disgust.value
    elif folder == 'fear':
        return PlaylistIDs.fear.value
    elif folder == 'happy':
        return PlaylistIDs.happy.value
    elif folder == 'sad':
        return PlaylistIDs.sad.value
    elif folder == 'surprise':
        return PlaylistIDs.surprise.value
    else:
        return random.choice(list(PlaylistIDs)).value


class YaMusic:

    def __init__(self, playlists=None):
        if playlists is None:
            playlists = []
        self.client = Client('AQAAAAA1CDveAAG8XoBLnveJl0FUtkL1ray9tU8').init()
        self.existing = []
        self.playlists = playlists

    def download_track(self, playlist):
        track_list = self.client.users_playlists(playlist).tracks
        track_count = len(track_list)
        track_num = random.randint(0, track_count - 1)

        track = track_list[track_num].fetch_track()
        track_name = track.title.replace('?', '')
        if track_name in self.existing:
            self.download_track(playlist)
            return
        track_artists = track.artists
        artists = []
        title = ''
        for artist in track_artists:
            artists.append(artist.name)
            if len(artists) == len(track_artists):
                title += artist.name + ' - '
                break
            title += artist.name + ', '
        title += track_name + '.mp3'
        self.existing.append(track_name)
        track.download(title)
        return title

    def download_all_tracks(self):
        for playlist in self.playlists:
            self.download_track(playlist)

    def clear(self):
        self.existing = []

    def get_list(self):
        return self.existing
