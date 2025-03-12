import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from tabulate import tabulate

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

### https://developers.google.com/youtube/v3/quickstart/python

def get_youtube_object():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    #os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "yt_secret.json"

    # Get credentials and create an API client
    
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_local_server(port=0)
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)
    return youtube


def get_video_list(youtube, playlist_url):
    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        maxResults=100,
        playlistId=playlist_url
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
    youtube = get_youtube_object()
    video_ids = get_video_list(youtube, "PLypkurRr2080AquOd7AO3fhdJXuiGZ8Of")
    videos = get_videos(youtube, video_ids)
    
    table = []
    for video in videos:
        #video["snippet"]["title"]
        #video["contentDetails"]["duration"]
        table.append([video["snippet"]["title"],video["contentDetails"]["duration"]])
        
    print("")
    print(tabulate(table, headers=["Title","Duration"], tablefmt="grid"))
    print("")
    

if __name__ == "__main__":
    main()