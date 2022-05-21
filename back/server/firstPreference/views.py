from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

# 초기 추천


@csrf_exempt
def prefer(request):
    # 메뉴 내보내기
    if request.method == 'GET':
        return HttpResponse(status=200)
    # 메뉴 클릭한 것 받아오기
    elif request.method == 'POST':
        return HttpResponse(status=201)
    else:
        return HttpResponse(status=400)
