import asyncio
import json
import os
import random

from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache
from dotenv import load_dotenv
from openai import OpenAI

from CraneUtils.websockets import receive_handler, transmit


class ConnectConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.all_client = {}
        self.state = 'transmit'

    async def websocket_connect(self, message):
        await self.accept()
        cache.set('ComputingUnit', self.channel_name, timeout=60 * 60 * 24)

    async def websocket_disconnect(self, message):
        pass

    async def websocket_receive(self, message):
        await receive_handler(self, message)

    async def handle_create_pipe(self, data):
        message = json.dumps({
            'commend': 'signal',
            'signal': 'create_pipe',
            'data': data
        })
        await self.send(text_data=message)

    async def handle_error(self, data):
        print(data)


# 定义多通道
class PipeConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target_client = None
        self.state = 'connect'

    async def websocket_connect(self, message):
        await self.accept()

    async def websocket_receive(self, message):
        await receive_handler(self, message)

    async def handle_connect(self, data):
        self.target_client = data
        await transmit(self, target=data, text=json.dumps({
            'commend': 'signal',
            'signal': 'pipe_distributed',
            'data': self.channel_name
        }))

    async def handle_close(self, data):
        await self.send(text_data=json.dumps({
            'commend': 'stop_voice_recognition',
        }))

    async def trigger_voice_recognition(self, data):
        message = json.dumps({
            'commend': 'start_voice_recognition',
        })
        await self.send(text_data=message)

    async def handle_voice_recognition(self, data):
        data = data["bytes"]
        await self.send(bytes_data=data)

    async def handle_voice_talk(self, data):
        pass

    async def handle_error(self, data):
        print(data)


class DeepSeekConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.deepseek = DeepSeek()

    async def websocket_connect(self, message):
        await self.accept()

    async def websocket_receive(self, message):
        await receive_handler(self, message)

    async def handle_error(self, data):
        print(data)

    async def handle_message(self, data):
        await self.deepseek.websocket_chat(data, self.send)


class DeepSeek:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("api_key")
        self.client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        self.history = [
            {"role": "system",
             "content": "你是一个智音手环的智能助手，为用户提供健康上的帮助,请不要用表情。user当前心跳83,血氧98,当前状态:静坐，不要使用markdown，模仿实际对话的方式回答问题。"},
        ]
        self.stream = True
        self.model = "deepseek-chat"

    # noinspection PyTypeChecker
    async def websocket_chat(self, message, send_func):
        self.history.append({"role": "user", "content": message})
        content = ''
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.history,
            stream=self.stream
        )

        if self.stream:
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    delta = chunk.choices[0].delta.content
                    content += delta
                    await send_func(delta)
                    await asyncio.sleep(random.randint(0, 3) / 10)
        else:
            content = response.choices[0].message.content
            await send_func(content)
        self.history.append({"role": "assistant", "content": content})

    async def chat_test(self, send_func):
        content = list('API 是一个“无状态” API，即服务端不记录用户请求的上下文，用户在每次请求时')
        for i in content:
            await send_func(i)
            await asyncio.sleep(random.randint(0, 3) / 10)
