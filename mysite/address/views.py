from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Address
from .serializers import AddressSerializer
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


@csrf_exempt
def address_list(request):
    if request.method == 'GET':
        query_set = Address.objects.all()
        serializer = AddressSerializer(query_set, many=True)
        return JsonResponse(serializer.data, content_type=u"application/json; charset=utf-8", safe=False)

    elif request.method == 'POST':  #
        # im = Image.open("1.png") # REST로 받아야 됨
        # text = pytesseract.image_to_string(im, lang="Hangul")

        data = JSONParser().parse(request)
        serializer = AddressSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
