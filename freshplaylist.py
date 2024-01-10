from job import JobInterface
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import datetime


class FreshPlaylist(JobInterface):
    def __init__(self, original_playlist: str, fresh_playlist: str, duration: int = 30):
        """
        :param original_playlist: The name of the playlist that the fresh one should be based on
        :param fresh_playlist: The name of the fresh playlist
        :param duration: The expiration duration for tracks in days
        """
        self.original_playlist = original_playlist
        self.fresh_playlist = fresh_playlist
        self.duration = duration
        self.scope = ['user-library-read',
                      # 'user-read-recently-played',
                      # 'user-read-currently-playing',
                      'playlist-read-private',
                      'playlist-modify-private',
                      'playlist-modify-public',
                      # 'user-top-read'
                      ]

    def run(self):
        """
        The job of the script
        """
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=self.scope))

        user_id = sp.current_user()['id']

        # Find the playlist that should be worked on
        original_playlist_id = None
        fresh_playlist_id = None
        playlists = sp.current_user_playlists()

        for _, item in enumerate(playlists['items']):
            if item['name'] == self.original_playlist:
                original_playlist_id = item['id']
            if item['name'] == self.fresh_playlist:
                fresh_playlist_id = item['id']

        # Double check to make sure that the original playlist was found
        if original_playlist_id:
            pass
        else:
            print(f'Playlist not found! -> {self.original_playlist}')
            quit()

        # Double check to make sure the fresh playlist exists, else make it
        if fresh_playlist_id:
            pass
        else:
            print(f'Playlist not found! -> {self.fresh_playlist}')
            print('Creating playlist ...')
            description = f'A list of songs added to {self.original_playlist} within {self.duration} days.'
            sp.user_playlist_create(user=user_id, name=self.fresh_playlist, description=description)
            playlists = sp.current_user_playlists()
            for _, item in enumerate(playlists['items']):
                if item['name'] == self.fresh_playlist:
                    fresh_playlist_id = item['id']

        tracks_in_playlist = sp.playlist_items(original_playlist_id, additional_types=("track",))
        tracks = tracks_in_playlist['items']

        items_to_keep = []
        for _, item in enumerate(tracks):
            added_time = datetime.datetime.strptime(item['added_at'], '%Y-%m-%dT%H:%M:%SZ')
            delta_time = datetime.datetime.utcnow() - added_time
            if delta_time <= datetime.timedelta(
                    days=self.duration):  # If the item was added a certain time ago, add to delete list
                items_to_keep.append(item)

        # Make a list of ids to add to the fresh playlist
        ids_to_keep = []
        for item in items_to_keep:
            ids_to_keep.append(item['track']['id'])

        fresh_tracks_in_playlist = sp.playlist_items(fresh_playlist_id, additional_types=("track",))
        fresh_tracks = fresh_tracks_in_playlist['items']

        # Make a list of all ids to remove from the fresh playlist
        ids_to_remove = []
        for item in fresh_tracks:
            ids_to_remove.append(item['track']['id'])

        # Remove all songs in fresh playlist
        sp.playlist_remove_all_occurrences_of_items(fresh_playlist_id, ids_to_remove)
        if len(ids_to_keep) != 0:
            sp.playlist_add_items(fresh_playlist_id, ids_to_keep)
