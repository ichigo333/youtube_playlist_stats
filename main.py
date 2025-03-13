import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from tabulate import tabulate
from duration_helper import parse_duration
from datetime import timedelta



### https://developers.google.com/youtube/v3/quickstart/python

def get_youtube_object(credentials):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    #os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    
    api_service_name = "youtube"
    api_version = "v3"
           
    youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)
    return youtube


def get_credentials(client_secrets_file, token_file):
    scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
    credentials = None

    # Get credentials and create an API client
    if os.path.exists(token_file):
        credentials = Credentials.from_authorized_user_file(token_file, scopes)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
            credentials = flow.run_local_server(port=0)
        
        with open(token_file, "w") as token:
            token.write(credentials.to_json())
    return credentials


def get_video_list(youtube, playlist_url):
    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        maxResults=100,
        playlistId=playlist_url,
    )
    response = request.execute()

    video_ids = ""
    for item in response["items"]:
        video_ids += f"{item["contentDetails"]["videoId"]},"
    return video_ids


def get_videos(youtube, video_ids):
    request = youtube.videos().list(
        part="snippet,contentDetails",
        maxResults=100,
        id=video_ids
    )
    
    response = request.execute()
    return response["items"]


def main():
    # TODO: move to config file?
    client_secrets_file = "yt_secret.json"
    token_file = "token.json"
    play_list_id = "PLypkurRr2083IrhT5fY7fFXstnx3fgfD6"
    #--------------------------------------------------#
    
    credentials = get_credentials(client_secrets_file, token_file)
    youtube = get_youtube_object(credentials)
    video_ids = get_video_list(youtube, play_list_id)
    videos = get_videos(youtube, video_ids)
    
    table = []
    total_time = timedelta()
    for video in videos:
        title = video["snippet"]["title"]
        duration = parse_duration(video["contentDetails"]["duration"][2:])
        table.append([title,duration])
        total_time += duration
        
    print("")
    print(tabulate(table, headers=["Title","Duration"], tablefmt="github"))
    print("")
    print(f"Total time: {total_time}")
    print("")
    

if __name__ == "__main__":
    main()