from datetime import datetime
import os
import isodate

from googleapiclient.discovery import build


class PlayList:
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, id_playlist):
        self.__id_playlist = id_playlist
        self.__playlist = self.youtube.playlists().list(id=self.__id_playlist,
                                                        part='snippet,contentDetails').execute()
        self.title = self.__playlist['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.__id_playlist}'
        playlist_videos = self.youtube.playlistItems().list(playlistId=self.__id_playlist,
                                                            part='contentDetails',
                                                            maxResults=50, ).execute()

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        self.__video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                           id=','.join(video_ids)).execute()

    @property
    def total_duration(self):

        all_duration = isodate.parse_duration(self.__video_response['items'][0]['contentDetails']['duration'])

        for video in self.__video_response['items'][1:]:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            all_duration += duration
        return all_duration

    def show_best_video(self):
        most_popular_video = self.__video_response['items'][0]['statistics']['likeCount']
        best_index = 0

        for index, video in enumerate(self.__video_response['items'][1:]):
            if video['statistics']['likeCount'] > most_popular_video:
                most_popular_video = video['statistics']['likeCount']
                best_index = index + 1

        return f'https://youtu.be/{self.__video_response['items'][best_index]['id']}'
