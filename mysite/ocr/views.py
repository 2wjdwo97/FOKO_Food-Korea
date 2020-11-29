from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from PIL import Image
from .forms import ReceiveImageForm
from food.models import Food, AllergyClass, FoodClass, MapFoodIngre, MapFoodIngreAdd, Ingredient
from ocr.stringDist import matchStr
from recommend.recommend import recommendFood
from food.views import calc_tags
import copy
from .googleCloudService import translate, extractText
import jwt


@csrf_exempt
def imageupload(request):
    if request.method == 'POST':
        # get image file
        form = ReceiveImageForm(request.POST, request.FILES)
        im = request.FILES['file'].read()

        texts = extractText(im)

        # get food list from models.py
        food_list = list(Food.objects.values_list('food_name', flat=True))

        # get match(between text list & food list) libst
        match_list = matchStr(texts[0].description, food_list, ratio_limit = 0.8)

        # get food description from models.py

        food_korName = match_list
        food_no = []
        food_engName = []
        food_description = []
        food_img_url = []
        food_ingredients = []
        food_allergies = []
        recommend_idx = []
        food_star = []
        food_spicy = []
        food_tags = []

        for name in match_list:
            # append engName
            food_engName.append(translate(name))

            db_Food = Food.objects.get(food_name=name)
            # append img_url
            food_img_url.append(db_Food.food_img_url)
            # append star
            food_star.append(db_Food.food_star)
            # append spicy
            food_spicy.append(db_Food.food_spicy)
            description = db_Food.food_dsc
            # append description
            food_description.append(translate(description))
            food_number = db_Food.food_no

            food_tags.append(calc_tags(food_number, 0))
            food_no.append(food_number)

            ingre_numbers = MapFoodIngre.objects.filter(food_no=food_number).values_list('ingre_no', flat=True)
            db_FoodIngreAdd = MapFoodIngreAdd.objects.filter(food_no=food_number)
            if db_FoodIngreAdd.exists():
                ingre_numbers += db_FoodIngreAdd.values_list('ingre_no', flat=True)

            ingredients = []
            allergies = []
            for ingre_number in ingre_numbers:
                db_Ingre = Ingredient.objects.get(ingre_no=ingre_number)
                ingredients.append(db_Ingre.ingre_en_name)

                allergy_number = db_Ingre.allergy_no.allergy_no
                if allergy_number != 0:
                    allergy = AllergyClass.objects.get(allergy_no=int(allergy_number)).allergy_en_name
                    if allergy not in allergies:
                        allergies.append(allergy)
            # append ingredients
            food_ingredients.append(ingredients)
            # append allergies
            food_allergies.append(allergies)

        access_token = request.headers['access-token']
        user_number = jwt.decode(access_token, settings.SECRET_KEY, algorithm='HS256')['user_no']

        # get food rank
#        if request.COOKIES.get('user_number'):
#            user_number = request.COOKIES['user_number']
        __, sorted_score, idx_sorted_score = recommendFood(user_number, food_no)

#        for i in range(0, 3):
#            if sorted_score[i] < -3.5:
#                recommend_idx.append(idx_sorted_score[i])
#            else:
#                break
        recommend_idx = [idx_sorted_score[i] for i in range(0, 3) if sorted_score[i] < -3.5]
        recommend_food = [0] * len(food_korName)
        for i, idx in enumerate(recommend_idx):
            recommend_food[idx] = i + 1

        description = {
            "food_korName": food_korName,
            "food_engName": food_engName,
            "food_star": food_star,
            "food_spicy": food_spicy,
            "food_description": food_description,
            "food_ingredients": food_ingredients,
            "food_allergy": food_allergies,
            "recommend_food": recommend_food,
            "food_img_url": food_img_url,
            "food_tag" : food_tags,
        }

        return JsonResponse(description, status=201)
    elif request.method == 'GET':
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'PUT':
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        return JsonResponse(serializer.errors, status=400)
