from tabulate import tabulate
from duration_helper import parse_duration
from datetime import timedelta
from youtube_api import YoutubeApi


### https://developers.google.com/youtube/v3/quickstart/python

def main():
    # TODO: move to config file?
    client_secrets_file = "yt_secret.json"
    token_file = "token.json"
    play_list_id = "PLypkurRr2083IrhT5fY7fFXstnx3fgfD6"
    #--------------------------------------------------#
    
    api = YoutubeApi(client_secrets_file, token_file)
    video_ids = api.get_video_list(play_list_id)
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