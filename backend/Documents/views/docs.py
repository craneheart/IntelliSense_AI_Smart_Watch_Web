from django.views import View
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
import json
import base64


def docs(name):
    # TODO:添加检查,结合列表
    with open(f"Documents/Documents/{name}.pdf", 'rb') as f:
        file_data = f.read()
        encoded = base64.b64encode(file_data).decode('utf-8')
    return encoded


class DocsView(View):
    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        return JsonResponse(['Research_Report'], safe=False)

    def post(self, request):
        data = json.loads(request.body)
        encoded = docs(data['name'])
        return HttpResponse(encoded)
