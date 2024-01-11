from spotify_scripts.freshplaylist import FreshPlaylist
import pytest
import datetime

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
    
def test_run(mocker):
    mock_spotipy = mocker.patch('spotipy.Spotify')
    mock_spotipy.return_value.current_user.return_value = {"id": 1}
    mock_spotipy.return_value.current_user_playlists.return_value = {"items": [{'name': 'orig', 'id': 23}, {'name': 'new', 'id': 24}]}
    mock_spotipy.return_value.playlist_items.return_value = {"items": [{'added_at': datetime.datetime.strftime(datetime.datetime.now(datetime.UTC), '%Y-%m-%dT%H:%M:%SZ'), 'track': {'id': 2}}]}
    freshjob = FreshPlaylist('orig', 'new')
    freshjob.run()
    assert mock_spotipy.return_value.current_user.call_count == 1
    assert mock_spotipy.return_value.current_user_playlists.call_count == 1
    assert mock_spotipy.return_value.playlist_items.call_count == 2
    assert mock_spotipy.return_value.playlist_remove_all_occurrences_of_items.call_count == 1
    assert mock_spotipy.return_value.playlist_add_items.call_count == 1