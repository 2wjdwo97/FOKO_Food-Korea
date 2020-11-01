import numpy as np
# from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from food.models import MapFoodIngre, Ingredient
from user.models import User, MapUserAllergy


@csrf_exempt
def recommend_ocr(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            user_no = data['user_no']
            foods = data['food_no']

            # 음식별 점수
            foods_score = np.zeros(len(foods))

            # 사용자 알레르기
            user = User.objects.get(user_no=user_no)
            user_allergies = MapUserAllergy.objects.filter(user_no=user_no).values_list('allergy_no', flat=True)
            user_allergies = np.array(user_allergies)

            # 음식 알레르기
            food_allergies = []
            for i in range(len(foods)):
                food_no = foods[i]

                # MapFoodIngre.objects.filter(food_no=food_no).select_related('ingre_no').exclude(allergy_no=0).values_list('allergy_no', flat=True)
                ingredients = MapFoodIngre.objects.filter(food_no=food_no).values_list('ingre_no', flat=True)

                allergies = []
                for j in range(len(ingredients)):
                    allergy_no = Ingredient.objects.get(ingre_no=ingredients[j]).allergy_no.allergy_no
                    if allergy_no != 0:
                        allergies.append(allergy_no)

                food_allergies.append(np.unique(allergies))

            # 사용자 알레르기, 음식 알레르기 비교 후 같으면 점수 -1
            for i in range(len(food_allergies)):
                if np.intersect1d(food_allergies[i], user_allergies):
                    foods_score[i] = -1

            return JsonResponse({"message": "SUCCESS"}, status=200)

        except KeyError as ke:
            print(ke)
            return JsonResponse({"message": "INVALID_KEYS"}, status=400)
