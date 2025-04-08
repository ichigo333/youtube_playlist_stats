# youtube_playlist_stats
 
## Purpose

Test app to see how youtube API works.  Initially all it's doing is getting a list of videos in a playlist and adds up total playtime.

## Requirements

- See requirements.txt for non standard Python libraries that need to be installed
- Dev credentials/secrets file is required to access youtube api
  - See https://developers.google.com/youtube/v3/quickstart/python for instructions
  - See https://console.developers.google.com/apis/credentials console to create and download your secrets file
- config.json is required with
  - `client_secrets_file_name` - file name of the secrets file downloaded in previous step
  - `token_file_name` - file name to store temporary token for authentication.  Can be any name.  This file will be overwritten each time token expires and you need to re-authenticate
  - `playlist_id` - id of your playlist.  If this is left blank, the program will prompt you for id during runtime.
    - playlist **MUST BE** either **Public** or **Unlisted** (accessible with a link).  API doesn't seem to allow access of private lists even when authenticated.
    - **History** and **Watch Later** playlists are also not accessible through API.

### Config.json example

```
{
    "client_secrets_file_name" : "your_secrets_file.json",
    "token_file_name" : "token.json",
    "playlist_id" : ""
}
```