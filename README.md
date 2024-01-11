# Spotify App
A python package that creates spotify playlists for a user.
## Usage
Create a json file with the desired playlist jobs. You can make playlists that contain songs that were added to another playlist within the last N days using `fresh_playlists` and songs that contain your top N songs using `top_playlists`.

Then run:

```create-playlists [path_to_config.json]```
### Example config.json
```
{
    "fresh_playlists": [
        {
            "original_playlist": "Example playlist",
            "fresh_playlist": "Example playlist - last 30 days",
            "duration": 30
        },
        {
            "original_playlist": "Example playlist",
            "fresh_playlist": "Example playlist - last 10 days",
            "duration": 10
        }
    ],
    "top_playlists": [
        {
            "playlist_name": "Long term Top 50",
            "time_range": "long_term",
            "description": "Example description",
            "limit": 50
        },
        {
            "playlist_name": "Medium term Top 25",
            "time_range": "medium_term",
            "limit": 25
        },
        {
            "playlist_name": "Short term Top 10",
            "limit": 10
        }
    ]
}
```

## Python Environment
See `requirements.txt`.
## Required environment variables
- SPOTIPY_CLIENT_ID = 'client id'
- SPOTIPY_CLIENT_SECRET = 'client secret'
- SPOTIPY_REDIRECT_URI = 'uri' (Ex. http://localhost:8000)

May use a `.env` file at project root to define variables.