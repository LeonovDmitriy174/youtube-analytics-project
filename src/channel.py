import json
import os

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.__channel = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title: str = self.__channel['items'][0]['snippet']['title']
        self.description: str = self.__channel['items'][0]['snippet']['description']
        self.url = self.__channel['items'][0]['snippet']['thumbnails']['default']['url']
        self.subscribers: int = self.__channel['items'][-1]['statistics']['subscriberCount']
        self.video_count = self.__channel['items'][-1]['statistics']['videoCount']
        self.view_count = self.__channel['items'][-1]['statistics']['viewCount']

    @property
    def channel_id(self) -> str:
        return self.__channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.__channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API"""
        return build('youtube', 'v3', developerKey=cls.api_key)

    def to_json(self, file_name: str) -> None:
        """Сохраняет в файл значения атрибутов экземпляра Channel"""
        for_json: dict = {'title': self.title, 'description': self.description,
                          'url': self.url, 'subscribers': self.subscribers,
                          'video_count': self.video_count, 'view_count': self.view_count}
        with open(file_name, 'w') as file:
            json.dump(for_json, file)
