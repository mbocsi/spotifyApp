from spotify_scripts.freshplaylist import FreshPlaylist
import pytest
import datetime
from unittest.mock import patch, DEFAULT

@pytest.fixture
def mock_spotipy():
    config = {
        'current_user': DEFAULT,
        'current_user_playlists': DEFAULT,
        'playlist_items': DEFAULT,
        'playlist_remove_all_occurrences_of_items': DEFAULT,
        'playlist_add_items': DEFAULT
    }
    with patch.multiple('spotipy.Spotify', **config) as mocked_spotipy:
        mocked_spotipy['current_user'].return_value = {"id": 1}
        mocked_spotipy['current_user_playlists'].return_value = {"items": [{'name': 'orig', 'id': 23}, {'name': 'new', 'id': 24}]}
        mocked_spotipy['playlist_items'].return_value = {"items": [{'added_at': datetime.datetime.strftime(datetime.datetime.now(datetime.UTC), '%Y-%m-%dT%H:%M:%SZ'), 'track': {'id': 2}}]}
        yield mocked_spotipy

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
    
def test_run(mock_spotipy):
    freshjob = FreshPlaylist('orig', 'new')
    assert mock_spotipy['current_user'].call_count == 0
    assert mock_spotipy['current_user_playlists'].call_count == 0
    assert mock_spotipy['playlist_items'].call_count == 0
    assert mock_spotipy['playlist_remove_all_occurrences_of_items'].call_count == 0
    assert mock_spotipy['playlist_add_items'].call_count == 0
    freshjob.run()
    assert mock_spotipy['current_user'].call_count == 1
    assert mock_spotipy['current_user_playlists'].call_count == 1
    assert mock_spotipy['playlist_items'].call_count == 2
    assert mock_spotipy['playlist_remove_all_occurrences_of_items'].call_count == 1
    assert mock_spotipy['playlist_add_items'].call_count == 1