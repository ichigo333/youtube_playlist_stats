import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google.oauth2.credentials import Credentials
# from google.auth.transport.requests import Request

class YoutubeApi:
    
    def __init__(self, client_secrets_file, token_file):
        self.scopes = ["https://www.googleapis.com/auth/youtube.readonly"] 
        self.api_service_name = "youtube"
        self.api_version = "v3"
        self.client_secrets_file = client_secrets_file
        self.token_file = token_file
        self._credentials = None
        self._service = None
        
    @property
    def credentials(self):
        if self._credentials is None:
            self._credentials = self._get_credentials()
        return self._credentials

    @property
    def service(self):
        if self._service is None:
            self._service = self._get_youtube_service()
        return self._service
        
    def _get_credentials(self):
        credentials = None

        # Get credentials and create an API client
        if os.path.exists(self.token_file):
            credentials = Credentials.from_authorized_user_file(self.token_file, self.scopes)
        if not credentials or not credentials.valid:
            ### Credential refresh doesn't seem to be working, even though below code is from Google
            # if credentials and credentials.expired and credentials.refresh_token:
            #     credentials.refresh(Request())
            # else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(self.client_secrets_file, self.scopes)
            credentials = flow.run_local_server(port=0)

            with open(self.token_file, "w") as token:
                token.write(credentials.to_json())
        return credentials
    
    
    def _get_youtube_service(self):
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        #os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        
        service = googleapiclient.discovery.build(self.api_service_name, self.api_version, credentials=self.credentials)
        return service
    
    def get_video_list(self, playlist_url):
        request = self.service.playlistItems().list(
            part="snippet,contentDetails",
            maxResults=100,
            playlistId=playlist_url,
        )
        response = request.execute()

        video_ids = ""
        for item in response["items"]:

            id = item["contentDetails"]["videoId"]
            video_ids += f"{id},"
        return video_ids
    
    
    def get_videos(self, video_ids):
        request = self.service.videos().list(
            part="snippet,contentDetails",
            maxResults=100,
            id=video_ids
        )

        response = request.execute()
        return response["items"]