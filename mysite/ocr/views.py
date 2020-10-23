from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from PIL import Image
from .forms import ReceiveImageForm
import pytesseract
from ocr.imageProcess import runOCR
from ocr.textSimilarity import getTheMostSimilarText
from food.models import Food

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

        return JsonResponse(match_list, safe=False, status=201)
    elif request.method == 'GET':
        return JsonResponse('1', safe=False, status=201)
