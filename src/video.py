import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class Video:
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id):
        self.video_id = video_id
        video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                        id=self.video_id).execute()
        try:
            self.title: str = video_response['items'][0]['snippet']['title']
        except IndexError:
            self.title = None
            self.view_count = None
            self.like_count = None
            self.url_video = None
        else:
            self.view_count: int = video_response['items'][0]['statistics']['viewCount']
            self.like_count: int = video_response['items'][0]['statistics']['likeCount']
            self.url_video: str = f'https://youtu.be/{self.video_id}'

    def __str__(self):
        return self.title


class PLVideo(Video):

    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id: str = playlist_id
