import os
import json
from googleapiclient.discovery import build

from helper.youtube_api_manual import youtube
api_key: str = os.getenv('YT_API_KEY')

class Channel:
    """Класс для ютуб-канала"""

    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self.title = self.channel['items'][0]['snippet']['title']
        self.channel_description = self.channel['items'][0]['snippet']['description']
        self.url = f"https://www.youtube.com/channel/{self.channel['items'][0]['id']}"
        self.channel_qty_sub = self.channel['items'][0]['statistics']['subscriberCount']
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        self.channel_qty_views = self.channel['items'][0]['statistics']['viewCount']

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        return print(json.dumps(channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API"""
        return cls.youtube

    def to_json(self, filename):
        """Сохраняет значения атрибутов экземпляра Channel в файл в формате JSON."""
        data = {
            "channel_id": self.channel_id,
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
