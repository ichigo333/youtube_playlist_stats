from tabulate import tabulate
from config import Config
from duration_helper import parse_duration
from datetime import timedelta
from youtube_api import YoutubeApi


def main():
    config = Config("config.json")
    playlist_id = config.playlist_id
    if not playlist_id:
        playlist_id = input("Enter playlist id: ")
    
    api = YoutubeApi(config.client_secrets_file_name, config.token_file_name)
    video_ids = api.get_video_list(playlist_id)
    videos = api.get_videos(video_ids)
    
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