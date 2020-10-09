from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .serializers import SignupSerializer


def signup(request):
    if request.method == "POST":
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user(
                username=request.POST['username'], password=request.POST['password1'])
            auth.login(request, user)

            print("signup success!")
            return HttpResponse(status=200)
        else:
            print("password - not matched")
            return HttpResponse(status=400)
    else:
        print("not POST request")
        return HttpResponse(status=400)


@csrf_exempt
def login(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id', '')
        user_pw = request.POST.get('user_pw', '')

        print("id = " + user_id + " pw = " + user_pw)

        result = authenticate(username=user_id, password=user_pw)

        if result:
            print("login success!")
            return HttpResponse(status=200)
        else:
            print("login error!")
            return HttpResponse(status=400)

    return render(request, 'login/login.html')
