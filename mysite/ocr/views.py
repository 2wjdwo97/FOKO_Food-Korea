from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from PIL import Image
from .forms import ReceiveImageForm
from food.models import Food, AllergyClass, FoodClass, MapFoodIngre, MapFoodIngreAdd, Ingredient
from ocr.stringDist import matchStr
from recommend.recommend import recommendFood
import copy
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/ubuntu/proj/CRAFT_image/My.json"
from google.cloud import vision
from google.cloud import translate_v2 as translate


@csrf_exempt
def imageupload(request):
    if request.method == 'POST':
        # get image file
        form = ReceiveImageForm(request.POST, request.FILES)
        im = request.FILES['file'].read()

        client = vision.ImageAnnotatorClient()
        image = vision.Image(content=im)
        response = client.text_detection(image=image)
        texts = response.text_annotations

        # get food list from models.py
        food_list = list(Food.objects.values_list('food_name', flat=True))

        # get match(between text list & food list) list
        match_list = matchStr(texts[0].description, food_list, ratio_limit = 0.8)

        # get food description from models.py
        client_t = translate.Client()

        food_korName = match_list
        food_no = []
        food_engName = []
        food_description = []
        food_img_url = []
        food_ingredients = []
        food_allergies = []
        recommend_food = []

        for name in match_list:
            food_engName.append(client_t.translate(name, target_language='en')['translatedText'])

            db_Food = Food.objects.get(food_name=name)
            food_img_url.append(db_Food.food_img_url)

            description = db_Food.food_dsc
            food_description.append(client_t.translate(description, target_language='en')['translatedText'])
#            food_description.append(translator.translate(description).text)

            food_number = db_Food.food_no
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

            food_ingredients.append(ingredients)
            food_allergies.append(allergies)
        user_number = -1
        # get food rank
        if request.COOKIES.get('user_number'):
            user_number = request.COOKIES['user_number']
            __, sorted_score, idx_sorted_score = recommendFood(user_number, food_no)

            for i in range(0, 3):
                if sorted_score[i] < -3.5:
                    recommend_food.append(food_no[idx_sorted_score[i]])
                else:
                    break
        cookies = list(request.COOKIES.keys())
        description = {
            "food_korName": food_korName,
            "food_engName": food_engName,
            "food_description": food_description,
            "food_ingredients": food_ingredients,
            "food_allergy": food_allergies,
            "recommend_food": recommend_food,
            "food_img_url": food_img_url,
            "user_number" : user_number,
            "cookies": cookies,
        }

        return JsonResponse(description, status=201)
    elif request.method == 'GET':
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'PUT':
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        return JsonResponse(serializer.errors, status=400)
