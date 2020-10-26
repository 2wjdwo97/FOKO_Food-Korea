from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from PIL import Image
from .forms import ReceiveImageForm
from food.models import Food, AllergyClass, FoodClass, MapFoodIngre, MapFoodIngreAdd, Ingredient
import pytesseract
from ocr.imageProcess import runOCR
from ocr.textSimilarity import getTheMostSimilarText

# Create your views here.

@csrf_exempt
def imageupload(request):
    if request.method == 'POST':
        # get image file
        form = ReceiveImageForm(request.POST, request.FILES)
        im = Image.open(request.FILES['file'])

        # get text list from image
        text_list = runOCR(im)

        # get food list from models.py
        food_list = list(Food.objects.values_list('food_name', flat=True))

        # get match(between text list & food list) list
        match_list = getTheMostSimilarText(text_list, food_list)

        # get food description from models.py
        food_korName = match_list
        food_engName = []
        food_description = []
        food_ingredients = []
        food_allergies = []

        for name in match_list:
            food_engName.append(name)

            db_Food = Food.objects.get(food_name=name)
            food_description.append(db_Food.food_dsc)

            food_number = db_Food.food_no

            ingre_numbers = MapFoodIngre.objects.filter(food_no=food_number).values_list('ingre_no', flat=True)
            db_FoodIngreAdd = MapFoodIngreAdd.objects.filter(food_no=food_number)
            if db_FoodIngreAdd.exists():
                ingre_numbers += db_FoodIngreAdd.values_list('ingre_no', flat=True)

            ingredients = []
            allergies = []
            for ingre_number in ingre_numbers:
                db_Ingre = Ingredient.objects.get(ingre_no=ingre_number)
                ingredients.append(db_Ingre.ingre_en_name)

                allergy_number = db_Ingre.allergy_no
                if allergy_number != 0:
                    db_allergyClass = AllergyClass.objects.get(allergy_no=allergy_number)

                    if db_allergyClass.allergy_en_name not in allergies:
                        allergies.append(db_allergyClass.allergy_en_name)

            food_ingredients.append(ingredients)
            food_allergies.append(allergies)

        description = {
            "food_korName": food_korName,
            "food_engName": food_engName,
            "food_description": food_description,
            "food_ingredients": food_ingredients,
            "food_allergy": food_allergies
        }

#        match_list.append('=========================')
#        match_list += text_list
        return JsonResponse(description, status=201)
    elif request.method == 'GET':
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'PUT':
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        return JsonResponse(serializer.errors, status=400)
