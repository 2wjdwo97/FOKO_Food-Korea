from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Address
from .serializers import AddressSerializer
from rest_framework.parsers import JSONParser
# Create your views here.


@csrf_exempt
def address_list(request):
    if request.method == 'GET':
        query_set = Address.objects.all()
        serializer = AddressSerializer(query_set, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = AddressSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
