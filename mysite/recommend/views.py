# from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from .recommend import recommendFood
from food.views import get_foods_by_list
from user.models import User

@csrf_exempt
def recommend_ocr(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            user_no = data['user_no']
            foods = data['food_no']             # 음식
            lang_code = User.objects.get(user_no=user_no).lang_no.lang_code

            foods, __, __ = recommendFood(user_no, foods)
            data_foods = get_foods_by_list(foods, lang_code)

            return JsonResponse(data_foods, safe=False, status=200)

        except KeyError as ke:
            print(ke)
            return JsonResponse({"message": "INVALID_KEYS"}, status=400)
