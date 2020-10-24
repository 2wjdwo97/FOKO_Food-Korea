import bcrypt
import jwt

from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from food.models import FoodClass, AllergyClass
from review.models import Tag, MapUserTag
from .models import MapUserClass, MapUserAllergy, User
from .serializers import UserSerializer


# 유저 정보 가져오기
@csrf_exempt
def manage(request, pk):
    user_info = User.objects.get(pk=pk)

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
        return HttpResponse(status=202)


# 회원가입
@csrf_exempt
def signup(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)

        # 유효성 검사 (아이디 중복 검사 등)
        if not serializer.is_valid():
            print(serializer.errors)
            return HttpResponse(status=404)

        # 비밀번호 확인
        if data['user_pw'] != data['pw_confirm']:
            return HttpResponse(status=404)

        password = data['user_pw'].encode('utf-8')                  # 입력된 패스워드를 바이트 형태로 인코딩
        password_crypt = bcrypt.hashpw(password, bcrypt.gensalt())  # 암호화된 비밀번호 생성
        password_crypt = password_crypt.decode('utf-8')             # 비밀번호 암호화
        serializer.validated_data['user_pw'] = password_crypt

        # 데이터베이스 저장
        serializer.save()

        return HttpResponse(status=200)


# 로그인
@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)

        try:
            if not User.objects.filter(user_id=data['user_id']).exists():
                return HttpResponse(status=404)

            # 비밀번호 확인
            account = User.objects.get(user_id=data['user_id'])
            if bcrypt.checkpw(data['user_pw'].encode('utf-8'), account.user_pw.encode('utf-8')):
                token = jwt.encode({'user_id': account.user_id}, settings.SECRET_KEY, algorithm='HS256')
                token = token.decode('utf-8')

                return JsonResponse({'access_token': token}, status=200)
            else:
                return HttpResponse(status=404)

        except KeyError as ke:
            print(ke)
            return JsonResponse({"message": "INVALID_KEYS"}, status=400)


# 선호하는 태그, 알레르기 식재료 설정
@csrf_exempt
def set_user_taste(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)

        try:
            user = data['user']
            food_classes = data['food_class']
            tags = data['tag']
            allergy_classes = data['allergy']

            for food_class in food_classes:
                MapUserClass(
                    user_no=User.objects.get(user_no=user),
                    food_class_no=FoodClass.objects.get(food_class_no=food_class),
                ).save()

            for tag in tags:
                MapUserTag(
                    user_no=User.objects.get(user_no=user),
                    tag_no=Tag.objects.get(tag_no=tag),
                ).save()

            for allergy_class in allergy_classes:
                MapUserAllergy(
                    user_no=User.objects.get(user_no=user),
                    allergy_no=AllergyClass.objects.get(allergy_no=allergy_class),
                ).save()

            return HttpResponse(status=200)

        except KeyError as ke:
            print(ke)
            return HttpResponse(status=400)
