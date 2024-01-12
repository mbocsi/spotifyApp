from spotify_scripts.freshplaylist import FreshPlaylist
import pytest
import datetime
from unittest.mock import patch

def test_init():
    with pytest.raises(TypeError) as excinfo:
        freshjob = FreshPlaylist()
    
    assert str(excinfo.value) == "FreshPlaylist.__init__() missing 2 required positional arguments: 'original_playlist' and 'fresh_playlist'"

    freshjob = FreshPlaylist('orig', 'new')
    assert freshjob.original_playlist == 'orig'
    assert freshjob.fresh_playlist == 'new'
    assert freshjob.duration == 30
    assert freshjob.scope == ['user-library-read',
                                'playlist-read-private',
                                'playlist-modify-private',
                                'playlist-modify-public',
                                ]
    
    freshjob2 = FreshPlaylist('orig1', 'new1', duration=42)
    assert freshjob2.original_playlist == 'orig1'
    assert freshjob2.fresh_playlist == 'new1'
    assert freshjob2.duration == 42
    assert freshjob2.scope == ['user-library-read',
                                'playlist-read-private',
                                'playlist-modify-private',
                                'playlist-modify-public',
                                ]

@patch('spotipy.Spotify')
@patch('spotipy.oauth2.SpotifyAuthBase')
def test_run(spotifyOAuth, spotify):
    spotify.return_value.current_user.return_value = {"id": 1}
    spotify.return_value.current_user_playlists.return_value = {"items": [{'name': 'orig', 'id': 23}, {'name': 'new', 'id': 24}]}
    spotify.return_value.playlist_items.return_value = {"items": [{'added_at': datetime.datetime.strftime(datetime.datetime.utcnow(), '%Y-%m-%dT%H:%M:%SZ'), 'track': {'id': 2}}]}

    mock_spotipy=spotify.return_value

    freshjob = FreshPlaylist('orig', 'new')
    assert mock_spotipy.current_user.call_count == 0
    assert mock_spotipy.current_user_playlists.call_count == 0
    assert mock_spotipy.playlist_items.call_count == 0
    assert mock_spotipy.playlist_remove_all_occurrences_of_items.call_count == 0
    assert mock_spotipy.playlist_add_items.call_count == 0
    freshjob.run()
    assert mock_spotipy.current_user.call_count == 1
    assert mock_spotipy.current_user_playlists.call_count == 1
    assert mock_spotipy.playlist_items.call_count == 2
    assert mock_spotipy.playlist_remove_all_occurrences_of_items.call_count == 1
    assert mock_spotipy.playlist_add_items.call_count == 1