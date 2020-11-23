# from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from .recommend import recommendFood
from food.views import get_foods_by_list

@csrf_exempt
def recommend_ocr(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            user_no = data['user_no']
            foods = data['food_no']             # 음식

            foods, __, __ = recommendFood(user_no, foods)
            data_foods = get_foods_by_list(foods)
            # food_names = []
            # for i in range(len(foods)):
            #     food_names.append(Food.objects.get(food_no=foods[i]).food_name)
            #
            # data_foods = {
            #     # "message": "SUCCESS",
            #     # "food_no": foods.tolist(),
            #     "food_name": food_names
            # }

            return JsonResponse(data_foods, safe=False, status=200)

        except KeyError as ke:
            print(ke)
            return JsonResponse({"message": "INVALID_KEYS"}, status=400)
