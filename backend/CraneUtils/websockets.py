import json

from django.core.cache import cache


async def run_handler(self, message, signal=False):
    if signal:
        handler = getattr(self, f'handle_{signal}', self.handle_error)
    else:
        handler = getattr(self, f'handle_{self.state}', self.handle_error)
    await handler(message)


async def trigger(self, trigger_name, data):
    handler = getattr(self, f'trigger_{trigger_name}', None)
    if handler:
        await handler(data)


async def receive_handler(self, message):
    if "text" not in message:
        await run_handler(self, message)
        return
    # 触发条件: 文字消息+"commend"字段正确
    data = json.loads(message['text'])
    commend = data.get('commend')
    if commend == 'switch_state':
        await trigger(self, data.get('state'), data.get('data'))
        self.state = data.get('state', "error")
    elif commend == "signal":
        await trigger(self, data.get('signal'), data.get('data'))
        signal = data.get('signal')
        data = data.get('data')
        await run_handler(self, data, signal=signal)
    else:
        await run_handler(self, message)
        return
    return


async def create_pipe_application(self):
    computing_unit = cache.get('ComputingUnit')
    await transmit(self, target=computing_unit, text=json.dumps({
        'commend': 'signal',
        'signal': 'create_pipe',
        'data': self.channel_name})
                   )


async def transmit(self, target, text=None, bytes_data=None):
    message = {
        'type': 'websocket.receive',
    }
    if text:
        message['text'] = text
    if bytes_data:
        message['bytes'] = bytes_data
    await self.channel_layer.send(target, message)
