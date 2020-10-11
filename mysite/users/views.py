import bcrypt
import jwt

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from foods.models import Classes, AllergyClasses
from mysite.settings import SECRET_KEY
from reviews.models import Tags, MapUserTag
from .models import Users, Countries, MapUserClass, MapUserAllergy
from .serializers import UserSerializer


# 유저 정보 가져오기
@csrf_exempt
def manage_user(request, pk):
    user_info = Users.objects.get(pk=pk)

    if request.method == "GET":
        serializer = UserSerializer(user_info)
        return JsonResponse(serializer.data, safe=False)

    # TODO 회원 정보 수정
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = UserSerializer(user_info, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    # TODO 회원 정보 삭제
    elif request.method == 'DELETE':
        # user_info.delete()
        return HttpResponse(status=204)


# 회원가입
@csrf_exempt
def signup(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)

        if serializer.is_valid():                       # TODO 유효성 검사 (중복 아이디 검사, 비밀번호 확인 등)
            password = data['user_pw'].encode('utf-8')                  # 입력된 패스워드를 바이트 형태로 인코딩
            password_crypt = bcrypt.hashpw(password, bcrypt.gensalt())  # 암호화된 비밀번호 생성
            password_crypt = password_crypt.decode('utf-8')             # 비밀번호 암호화

            # serializer.save()
            Users(
                user_id=data['user_id'],
                user_pw=password_crypt,
                user_name=data['user_name'],
                user_age=data['user_age'],
                user_spicy=data['user_spicy'],
                country_no=Countries.objects.get(country_no=data['country_no']),
            ).save()

            return HttpResponse(status=200)
        else:
            print(serializer.errors)
            return HttpResponse(status=400)


# 로그인
@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        # serializer = LoginSerializer(data=data)

        try:
            if Users.objects.filter(user_id=data['user_id']).exists():
                account = Users.objects.get(user_id=data['user_id'])

                # 비밀번호 확인
                if bcrypt.checkpw(data['user_pw'].encode('utf-8'), account.user_pw.encode('utf-8')):
                    token = jwt.encode({'user_id': account.user_id}, SECRET_KEY, algorithm='HS256')
                    token = token.decode('utf-8')
                    return JsonResponse({'access_token': token}, status=200)
                else:
                    return HttpResponse(status=401)

            return HttpResponse(status=400)

        except KeyError as ke:
            print(ke)
            return JsonResponse({"message": "INVALID_KEYS"}, status=400)


# 선호하는 태그, 알레르기 식재료 설정
@csrf_exempt
def set_user_taste(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)

        try:
            user_no = data['user_no']
            tags = data['tag'].split(',')
            food_classes = data['food_class'].split(',')
            allergy_classes = data['allergy'].split(',')

            for tag in tags:
                MapUserTag(
                    user_no=Users.objects.get(user_no=user_no),
                    tag_no=Tags.objects.get(tag_no=tag),
                ).save()

            for food_class in food_classes:
                MapUserClass(
                    user_no=Users.objects.get(user_no=user_no),
                    class_no=Classes.objects.get(class_no=food_class),
                ).save()

            for allergy_class in allergy_classes:
                MapUserAllergy(
                    user_no=Users.objects.get(user_no=user_no),
                    allergy_no=AllergyClasses.objects.get(allergy_no=allergy_class),
                ).save()

            return HttpResponse(status=200)

        except KeyError as ke:
            print(ke)
            return HttpResponse(status=200)
