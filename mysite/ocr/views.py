from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from PIL import Image
from .forms import ReceiveImageForm
import pytesseract
from ocr.imageProcess import runOCR

# Create your views here.

@csrf_exempt
def imageupload(request):
    if request.method == 'POST':
        # CRAFT
        # Tesseract
        form = ReceiveImageForm(request.POST, request.FILES)
        im = Image.open(request.FILES['file'])
        text = runOCR(im)

        return JsonResponse(text, safe=False, status=201)
    elif request.method == 'GET':
        return JsonResponse('1', safe=False, status=201)
