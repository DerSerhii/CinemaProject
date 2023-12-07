import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from channels.db import database_sync_to_async
from datetime import datetime

from cinema.models import Showtime


class NowShowtimesPlayingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        while True:
            # Obtaining current data
            now_showtime_playing_data = await self.get_now_showtimes_playing_data()
            print(now_showtime_playing_data)

            await self.send(text_data=json.dumps(now_showtime_playing_data))
            await asyncio.sleep(60)

    @database_sync_to_async
    def get_now_showtimes_playing_data(self):
        now = datetime.now()
        current_showtimes = Showtime.objects.filter(start__lte=now, end__gte=now)
        print('current_showtimes', current_showtimes)

        if current_showtimes.exists():
            film_titles = ', '.join(showtime.film.title for showtime in current_showtimes)
            now_playing_data = {
                'film_title': film_titles,
                'start_time': current_showtimes.first().start.strftime('%Y-%m-%d %H:%M:%S')
            }
        else:
            now_playing_data = {
                'film_title': 'No film playing',
                'start_time': now.strftime('%Y-%m-%d %H:%M:%S')
            }
        return now_playing_data


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'message': message
        }))