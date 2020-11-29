from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from ocr import googleCloudService
from user.models import User, MapUserEat
from food.views import get_foods_by_list
from food.models import Food
from review.models import Review, Tag, MapFoodTag
from review.serializers import ReviewSerializer


# 모든 리뷰 가져오기
@csrf_exempt
def get_all_review(request):
    if request.method == "GET":
        reviews = list(Review.objects.values())
        return JsonResponse(reviews, safe=False, status=200)


# 사용자가 작성한 리뷰 가져오기
@csrf_exempt
def get_user_review(request):
    if request.method == "POST":
        try:
            data = JSONParser().parse(request)
            user_no = data['user_no']
            lang_code = User.objects.get(user_no=user_no).lang_no.lang_code

            reviews = Review.objects.filter(user_no=user_no)
            review_list = []
            if reviews.exists():
                for review in reviews.values():
                    food = Food.objects.get(food_no=review['food_no_id'])
                    review['food_name'] = food.food_name
                    review['translated_name'] = googleCloudService.translate(food.food_name, lang_code)
                    review['food_img_url'] = food.food_img_url
                    review_list.append(review)

                return JsonResponse(review_list, safe=False, status=200)
            else:
                return JsonResponse([], safe=False, status=201)

        except KeyError:
            return JsonResponse({"message": "INVALID_KEY"}, status=400)


# 리뷰 저장
@csrf_exempt
def save_review(request):
    if request.method == "POST":
        try:
            data = JSONParser().parse(request)
            serializer = ReviewSerializer(data=data)

            user_no = data['user_no']
            food_no = Food.objects.get(food_name=data['food_name']).food_no
            serializer.initial_data['food_no'] = food_no

            # 먹은 음식의 후기 작성 여부 변경
            eaten_food = MapUserEat.objects.filter(user_no=user_no).get(food_no=food_no)
            if eaten_food.is_written == 1:
                return JsonResponse({"message": "ALREADY_WRITTEN"}, status=401)

            eaten_food.is_written = 1
            eaten_food.save()

            # 유효성 검사
            if not serializer.is_valid():
                print(serializer.errors)
                return JsonResponse({"message": "INVALID_FORM"}, status=402)

            # 리뷰 저장
            serializer.save()

            # 최근에 저장된 리뷰를 가져옴
            review = Review.objects.order_by('rev_no').last()

            # 음식 정보 업데이트 (평균 별점, 후기 수)
            food = Food.objects.get(food_no=food_no)
            star = food.food_star
            spicy = food.food_spicy
            cnt = food.food_review_count

            food.food_spicy = round(((spicy * cnt) + serializer.validated_data['rev_spicy']) / (cnt + 1), 1)
            food.food_star = round(((star * cnt) + serializer.validated_data['rev_star']) / (cnt + 1), 1)
            food.food_review_count = cnt + 1
            food.save()

            # 음식 태그 추가
            tags = data['tag_no']
            for i in range(len(tags)):
                MapFoodTag(
                    rev_no=Review.objects.get(rev_no=review.rev_no),
                    food_no=Food.objects.get(food_no=food_no),
                    tag_no=Tag.objects.get(tag_no=tags[i])
                ).save()

            return JsonResponse({"message": "SAVE_SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"message": "INVALID_KEY"}, status=400)


# 사용자가 먹은 음식 저장
@csrf_exempt
def save_eaten_food(request):
    try:
        if request.method == "POST":
            data = JSONParser().parse(request)
            user_no = data['user_no']
            foods = data['food_name']   # food list

            for food_name in foods:
                food = Food.objects.get(food_name=food_name)
                if not MapUserEat.objects.filter(user_no=user_no).filter(food_no=food.food_no).exists():
                    MapUserEat(
                        user_no=User.objects.get(user_no=user_no),
                        food_no=Food.objects.get(food_name=food_name)
                    ).save()

        return JsonResponse({"message": "SAVE_SUCCESS"}, safe=False, status=200)

    except KeyError:
        return JsonResponse({"message": "INVALID_KEY"}, status=400)


# 사용자가 먹은 음식 가져오기
@csrf_exempt
def get_eaten_food(request):
    try:
        if request.method == "POST":
            data = JSONParser().parse(request)
            user_no = data['user_no']
            lang_code = User.objects.get(user_no=user_no).lang_no.lang_code

            # 최신순으로 사용자가 먹은 음식 가져오기
            query_set = MapUserEat.objects.filter(user_no=user_no).order_by('-id')

            foods = query_set.filter(is_written=False).values_list('food_no', flat=True)
            # is_written = query_set.values_list('is_written', flat=True)

            eaten_food = get_foods_by_list(foods, lang_code)

            return JsonResponse(eaten_food, safe=False, status=200)

    except KeyError:
        return JsonResponse({"message": "INVALID_KEY"}, status=400)
