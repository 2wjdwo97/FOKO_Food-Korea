import string
import random
import bcrypt
import jwt

from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
# from django.core.validators import validate_email
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text

from rest_framework.parsers import JSONParser

from food.models import FoodClass, AllergyClass
from review.models import Tag, MapUserTag
from .models import MapUserFoodClass, MapUserAllergy, User
from .serializers import UserSerializer
from .tokens import account_activation_token
from .text import msg_Email


# 회원가입
@csrf_exempt
def signup(request):
    if request.method == "POST":
        try:
            data = JSONParser().parse(request)
            serializer = UserSerializer(data=data)

            # 유효성 검사 (아이디/이메일 중복 검사 등)
            if not serializer.is_valid():
                print(serializer.errors)
                return JsonResponse({"message": "INVALID_FORM"}, status=401)

            # 비밀번호 확인
            if data['user_pw'] != data['pw_confirm']:
                return JsonResponse({"message": "INVALID_PASSWORD"}, status=402)

            password = data['user_pw'].encode('utf-8')                  # 입력된 패스워드를 바이트 형태로 인코딩
            password_crypt = bcrypt.hashpw(password, bcrypt.gensalt())  # 암호화된 비밀번호 생성
            password_crypt = password_crypt.decode('utf-8')             # 비밀번호 암호화
            serializer.validated_data['user_pw'] = password_crypt

            # 데이터베이스 저장
            serializer.save()

            # 이메일 인증
            user = User.objects.get(user_id=data['user_id'])

            current_site = get_current_site(request)
            domain = current_site.domain
            uidb64 = urlsafe_base64_encode(force_bytes(user.user_no))
            token = account_activation_token.make_token(user)

            message_data = msg_Email(domain, uidb64, token)
            mail_title = "Please complete the email verification."
            mail_to = serializer.data['user_email']
            email = EmailMessage(mail_title, message_data, to=[mail_to])
            email.send()

            return JsonResponse({"message": "SUCCESS"}, status=200)
        except KeyError:
            return JsonResponse({"message": "INVALID_KEY"}, status=403)


# 회원가입 인증
@csrf_exempt
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(user_no=uid)

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request)
            return JsonResponse({"message": "AUTH_SUCCESS"}, status=200)

        return JsonResponse({"message": "AUTH_FAIL"}, status=400)

    except KeyError:
        return JsonResponse({"message": "INVALID_KEY"}, status=400)
    except ValidationError:
        return JsonResponse({"message": "TYPE_ERROR"}, status=400)


# 로그인
@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)

        try:
            # 아이디 확인
            if not User.objects.filter(user_id=data['user_id']).exists():
                return JsonResponse({"message": "INVALID_ID"}, status=401)

            # 비밀번호 확인
            user = User.objects.get(user_id=data['user_id'])
            if not bcrypt.checkpw(data['user_pw'].encode('utf-8'), user.user_pw.encode('utf-8')):
                return JsonResponse({"message": "INVALID_PASSWORD"}, status=402)

            # 계정 활성화 확인
            if user.is_active == 0:
                return JsonResponse({"message": "NOT_ACTIVATE_ACCOUNT"}, status=402)

            token = jwt.encode({'user_id': user.user_id}, settings.SECRET_KEY, algorithm='HS256')
            token = token.decode('utf-8')

            if user.is_first == 1:
                return JsonResponse({"access_token": token}, status=201)
            else:
                return JsonResponse({'access_token': token}, status=200)

        except KeyError as ke:
            print(ke)
            return JsonResponse({"message": "INVALID_KEYS"}, status=400)


# 아이디 찾기
@csrf_exempt
def find_id(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)

        try:
            # 이메일 확인
            if not User.objects.filter(user_email=data['user_email']).exists():
                return JsonResponse({"message": "INVALID_EMAIL"}, status=401)

            # 이메일 전송
            user = User.objects.get(user_email=data['user_email'])
            mail_title = "Your ID from FOORI has been sent."
            email = EmailMessage(mail_title, user.user_id, to=[user.user_email])
            email.send()

            return JsonResponse({"message": "SEND_MAIL_SUCCESS"}, status=200)

        except KeyError as ke:
            print(ke)
            return JsonResponse({"message": "INVALID_KEYS"}, status=400)


# 비밀번호 찾기
@csrf_exempt
def find_pw(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)

        try:
            # 아이디 확인
            if not User.objects.filter(user_id=data['user_id']).exists():
                return JsonResponse({"message": "INVALID_ID"}, status=401)

            user = User.objects.get(user_id=data['user_id'])

            # 이메일 확인
            if user.user_email != data['user_email']:
                return JsonResponse({"message": "INVALID_EMAIL"}, status=401)

            user = User.objects.get(user_email=data['user_email'])

            # 임시 비밀번호 생성
            _LENGTH = 8
            temp_pw = ""
            for i in range(_LENGTH):
                temp_pw += random.choice(string.ascii_uppercase)

            # 암호화
            password = temp_pw.encode('utf-8')
            password_crypt = bcrypt.hashpw(password, bcrypt.gensalt())
            password_crypt = password_crypt.decode('utf-8')
            user.user_pw = password_crypt
            user.save()

            # 이메일 전송
            mail_title = "Your temporary password from FOORI has been sent."
            email = EmailMessage(mail_title, temp_pw, to=[user.user_email])
            email.send()

            return JsonResponse({"message": "SEND_MAIL_SUCCESS"}, status=200)

        except KeyError as ke:
            print(ke)
            return JsonResponse({"message": "INVALID_KEYS"}, status=400)


# 비밀번호 변경
@csrf_exempt
def change_pw(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)

        try:
            user = User.objects.get(user_no=data['user_no'])

            # 기존 비밀번호 확인
            if not bcrypt.checkpw(data['user_pw'].encode('utf-8'), user.user_pw.encode('utf-8')):
                return JsonResponse({"message": "INVALID_CURRENT_PASSWORD"}, status=401)

            # 비밀번호 확인
            if data['pw_new'] != data['pw_confirm']:
                return JsonResponse({"message": "INVALID_NEW_PASSWORD"}, status=402)

            user.user_pw = bcrypt.hashpw(data['pw_new'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            user.save()

            return JsonResponse({"message": "CHANGE_SUCCESS"}, status=200)

        except KeyError as ke:
            print(ke)
            return JsonResponse({"message": "INVALID_KEYS"}, status=400)


# 선호하는 태그, 알레르기 식재료 설정
@csrf_exempt
def set_user_taste(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)

        try:
            user = data['user_no']
            food_classes = data['food_class_no']
            tags = data['tag_no']
            allergy_classes = data['allergy_no']

            for food_class in food_classes:
                MapUserFoodClass(
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

            return JsonResponse({"message": "TASTE_SAVED"}, status=200)

        except KeyError as ke:
            print(ke)
            return JsonResponse({"message": "INVALID_KEY"}, status=400)


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
