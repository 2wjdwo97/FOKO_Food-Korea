from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .serializers import FoodSerializer
from .models import Food

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
def foods_list(request):
    if request.method == 'GET':
        query_set = Food.objects.all()
        serializer = FoodSerializer(query_set, many=True)
        return JsonResponse(serializer.data, safe=False)

        data = JSONParser().parse(request)
        serializer = FoodSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
