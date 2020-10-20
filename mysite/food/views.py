from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .serializers import FoodSerializer
from .models import Food


@csrf_exempt
def manage(request, pk):
    food_info = Food.objects.get(pk=pk)

    if request.method == "GET":
        serializer = FoodSerializer(food_info)
        return JsonResponse(serializer.data, safe=False)

    # TODO 음식 정보 수정
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = FoodSerializer(food_info, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    # TODO 음식 정보 삭제
    elif request.method == 'DELETE':
        # user_info.delete()
        return HttpResponse(status=204)
