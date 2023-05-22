import os
import json
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = self.channel['items'][0]['snippet']['title']
        self.channel_description = self.channel['items'][0]['snippet']['description']
        self.url = f"https://www.youtube.com/channel/{self.channel['items'][0]['id']}"
        self.channel_qty_sub = int(self.channel['items'][0]['statistics']['subscriberCount'])
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        self.channel_qty_views = self.channel['items'][0]['statistics']['viewCount']

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        return print(json.dumps(channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API"""
        return cls.youtube

    def to_json(self, filename):
        """Сохраняет значения атрибутов экземпляра Channel в файл в формате JSON."""
        data = {
            "channel_id": self.__channel_id,
            "title": self.title,
            "description": self.channel_description,
            "url": self.url,
            "subscriber_count": self.channel_qty_sub,
            "video_count": self.video_count,
            "view_count": self.channel_qty_views
        }

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
        return data

    @property
    def channel_id(self):
        return self.__channel_id

    def __str__(self):
        """Возвращающий название и ссылку на канал по шаблону"""
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        """Сложение количества подписчиков"""
        return self.channel_qty_sub + other.channel_qty_sub

    def __sub__(self, other):
        """Возвращает разность подписчиков двух объектов"""
        return self.channel_qty_sub - other.channel_qty_sub

    def __lt__(self, other):
        """Сравнение количества подписчиков меньше"""
        return self.channel_qty_sub < other.channel_qty_sub

    def __le__(self, other):
        """Сравнение количества подписчиков меньше или равно"""
        return self.channel_qty_sub <= other.channel_qty_sub

    def __gt__(self, other):
        """Сравнение количества подписчиков больше"""
        return self.channel_qty_sub > other.channel_qty_sub

    def __ge__(self, other):
        """Сравнение количества подписчиков больше или равно"""
        return self.channel_qty_sub >= other.channel_qty_sub

