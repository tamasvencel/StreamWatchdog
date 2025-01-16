import os
import time
from googleapiclient.discovery import build
from plyer import notification
from dotenv import load_dotenv

load_dotenv(dotenv_path="config.env")

YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")
# we can find the channel ID by sending request to the following endpoint:
# curl "https://www.googleapis.com/youtube/v3/search?part=snippet&type=channel&q=<CHANNEL_NAME>&key=<YOUTUBE_API_KEY>"
CHANNEL_ID = os.environ.get("CHANNEL_ID")

# Initialize YouTube API client
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)


def get_latest_video():
    # Fetch the latest video from the channel's uploads
    request = youtube.search().list(
        part='snippet',
        channelId=CHANNEL_ID,
        maxResults=1,
        order='date',
        type='video'
    )
    response = request.execute()

    latest_video = response['items'][0]
    video_id = latest_video['id']['videoId']
    video_title = latest_video['snippet']['title']
    return video_id, video_title


def notify(title, message):
    # Function to trigger desktop notification
    notification.notify(
        title=title,
        message=message,
        timeout=10  # Notification duration in seconds
    )


def main():
    last_video_id = None
    first_run = True

    while True:
        try:
            # Check for the latest video
            video_id, video_title = get_latest_video()

            # If the video ID is new, notify the user
            if not first_run and video_id != last_video_id:
                notify("Scheduled stream uploaded. Woohoo", f"{video_title} has been uploaded!")
                last_video_id = video_id

            first_run = False

            # Wait for 5 minutes before checking again
            time.sleep(300)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(60)


if __name__ == "__main__":
    main()
