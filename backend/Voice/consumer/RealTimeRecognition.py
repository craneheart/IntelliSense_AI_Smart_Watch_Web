from channels.generic.websocket import AsyncWebsocketConsumer
from CraneUtils.websockets import receive_handler, create_pipe_application, transmit
import json


class RealTimeRecognitionConsumer(AsyncWebsocketConsumer):
    def __init__(self):
        super().__init__()
        self.state = 'init'
        self.pipe = None
        self.application = None

    async def websocket_connect(self, message):
        await self.accept()

    async def websocket_disconnect(self, close_code):
        if self.pipe:
            await transmit(self, target=self.pipe, text=json.dumps({
                'commend': 'signal',
                'signal': 'close',
            }))

    async def websocket_receive(self, message):
        await receive_handler(self, message)

    async def handle_init(self, data):
        if self.pipe:
            await self.send(text_data=json.dumps({
                "commend": "signal",
                "signal": "ready",
            }))
        elif self.application:
            pass
        else:
            self.application = True
            await create_pipe_application(self)

    async def handle_pipe_distributed(self, data):
        self.pipe = data
        await self.send(text_data=json.dumps({
            "commend": "signal",
            "signal": "ready",
        }))

    async def trigger_voice(self, data):
        await transmit(self, target=self.pipe, text=json.dumps({
            'commend': 'switch_state',
            'state': 'voice_recognition',
        }))

    async def handle_voice(self, data):
        data = data["bytes"]
        await transmit(self, target=self.pipe, bytes_data=data)

    async def handle_close(self, data):
        await self.close()

    async def handle_error(self, data):
        print(f"error in RealTimeRecognitionConsumer:{data}")
