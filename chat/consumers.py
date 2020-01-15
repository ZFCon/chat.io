import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer


class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print('connected', event)
        print(self.scope["session"]["seed"])
        await self.channel_layer.group_add(
            'just2',
            self.channel_name,
            )
        await self.send({
            'type': 'websocket.accept',
        })

    async def websocket_receive(self, event):
        print('receive', event)
        data = event.get('text', None)
        if data != None:
            new_event = {
            'type':'chat.message',
            'message': data
            }
            await self.channel_layer.group_send(
                'just2',
                new_event
            )
    async def chat_message(self, event):
        await self.send({
            'type': 'websocket.send',
            'text': event.get('message')
        })

    async def websocket_disconnect(self, event):
        print('disconnected', event)