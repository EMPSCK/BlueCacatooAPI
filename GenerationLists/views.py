from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from . import logic
import json

@csrf_exempt
def get_competition_judges(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        ans = logic.get_ans(data)
        return JsonResponse(ans, safe=False)
