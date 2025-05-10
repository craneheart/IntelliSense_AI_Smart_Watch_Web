import asyncio
import json

import websockets

WS_URI = 'ws://localhost:8000/ws/computingUnit/'


class UnitAdmin:
    def __init__(self):
        self.websocket = None
        self.uri = WS_URI + 'connect/'

    async def connection(self):
        while True:
            try:
                async with websockets.connect(self.uri) as websocket:
                    self.websocket = websocket
                    print('ServerAdmin已连接')
                    await self.message_listener()
            except websockets.ConnectionClosed as e:
                print(f'ServerAdmin连接关闭: {e.code} - {e.reason}')
            except Exception as e:
                print(f'ServerAdmin连接错误: {str(e)}')

            print('3秒后尝试重连...')
            await asyncio.sleep(3)

    async def message_listener(self):
        while True:
            response = await self.websocket.recv()
            data = json.loads(response)
            print('ServerAdmin收到消息:', data)
            if data['commend'] == 'signal':
                await self.handle_signal(data)
            else:
                pass

    async def handle_signal(self, data):
        signal = data['signal']
        if signal == 'create_pipe':
            await self.create_pipe(target_channel_name=data['data'])
        else:
            pass

    async def create_pipe(self, target_channel_name):
        pipe = Pipe(target_channel_name)
        asyncio.create_task(pipe.connection())


class Pipe:
    def __init__(self, target_channel_name):
        self.target_channel_name = target_channel_name
        self.websocket = None
        self.file = False
        self.uri = WS_URI + 'pipe/'

    async def connection(self):
        async with websockets.connect(self.uri, max_size=None) as websocket:
            self.websocket = websocket
            print(f'创建新连接: {self.target_channel_name}')
            await self.websocket.send(json.dumps({
                'commend': 'signal',
                'signal': 'connect',
                'data': self.target_channel_name
            }))
            await self.listener()

    async def listener(self):
        try:
            while True:
                response = await self.websocket.recv()
                data = json.loads(response)
                commend = data.get('commend')
                if commend == 'start_voice_recognition':
                    await self.start_voice_recognition()
                else:
                    pass

        except websockets.ConnectionClosed as e:
            print(f'连接关闭: {e.code} - {e.reason}')

    async def start_voice_recognition(self):
        try:
            while True:
                response = await self.websocket.recv()
                # print(response)

        except websockets.ConnectionClosed as e:
            print(f'连接关闭: {e.code} - {e.reason}')
