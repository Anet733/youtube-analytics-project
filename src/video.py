import os
import json
from googleapiclient.discovery import build


class Video:

    def __init__(self, id_video):
        self.id_video = id_video
        self.video_response = self.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                               id=self.id_video).execute()
        self.title: str = self.video_response['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/watch?v={id_video}"
        self.view_count: int = self.video_response['items'][0]['statistics']['viewCount']
        self.like_count: int = self.video_response['items'][0]['statistics']['likeCount']

    def __str__(self):
        return self.title

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API"""
        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    @staticmethod
    def printj(dict_data) -> None:
        """Выводит словарь в json-подобном удобном формате с отступами"""
        print(json.dumps(dict_data, indent=2, ensure_ascii=False))


class PLVideo(Video):

    def __init__(self, id_video, playlist_id):
        self.playlist_id = playlist_id
        super().__init__(id_video)

    def playlist_response(self):
        return self.get_service().playlistItems().list(part='contentDetails',
                                                       maxResults=10,
                                                       playlistId=self.playlist_id
                                                       ).execute()
