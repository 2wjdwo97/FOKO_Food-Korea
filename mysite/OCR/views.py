from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from PIL import Image
from .forms import ReceiveImageForm
import pytesseract

# Create your views here.

@csrf_exempt
def imageUpload(request):
    if request.method == 'POST':
        # CRAFT
        
        # Tesseract
        form = ReceiveImageForm(request.POST, request.FILES)
        im = Image.open(request.FILES['file'])
        custom_oem_psm_config = r'--oem 3 --psm 7'
        text = pytesseract.image_to_string(im, lang="kor", config=custom_oem_psm_config)
        return JsonResponse(text, safe=False, status=201)

