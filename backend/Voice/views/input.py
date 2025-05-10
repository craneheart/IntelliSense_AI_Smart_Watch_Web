import base64
import datetime
import json
import os

from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

# 定义音频保存目录
AUDIO_SAVE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'audio_files')


@method_decorator(csrf_exempt, name='dispatch')
class Base64InputView(View):
    def get(self, request):
        return HttpResponse('1')

    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        audio_data = body_data.get('audio')
        print(audio_data)

        # Base64解码
        if audio_data:
            try:
                decoded_audio = base64.b64decode(audio_data)

                # 确保保存目录存在
                os.makedirs(AUDIO_SAVE_DIR, exist_ok=True)

                # 创建唯一文件名 (基于时间戳)
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                file_name = f"audio_{timestamp}.wav"
                file_path = os.path.join(AUDIO_SAVE_DIR, file_name)

                # 保存音频文件
                with open(file_path, 'wb') as f:
                    f.write(decoded_audio)

                print(f"解码成功，数据长度: {len(decoded_audio)} 字节")
                print(f"音频已保存至: {file_path}")

                return JsonResponse({
                    'status': 'success',
                    'message': '音频数据解码并保存成功',
                    'decoded_size': len(decoded_audio),
                    'file_path': file_path
                })
            except Exception as e:
                return JsonResponse({
                    'status': 'error',
                    'message': f'处理失败: {str(e)}'
                }, status=400)
        else:
            return JsonResponse({
                'status': 'error',
                'message': '未提供音频数据'
            }, status=400)
