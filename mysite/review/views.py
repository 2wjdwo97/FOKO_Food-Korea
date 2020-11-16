from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from user.models import User, MapUserEat
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

            reviews = Review.objects.filter(user_no=user_no)
            review_list = []
            if reviews.exists():
                for review in reviews.values():
                    review['food_name'] = Food.objects.get(food_no=review['food_no_id']).food_name
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
            cnt = food.food_review_count

            food.food_star = round(((star * cnt) + int(4)) / (cnt + 1), 1)
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
            foods = data['food_name']

            # MapUserEat(user_no=User.objects.get(user_no=user_no), food_no

            for food_name in foods:
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

            # 최신순으로 사용자가 먹은 음식 가져오기
            query_set = MapUserEat.objects.filter(user_no=data['user_no']).order_by('-id')

            foods = query_set.filter(is_written=False).values_list('food_no', flat=True)
            # is_written = query_set.values_list('is_written', flat=True)

            eaten_food = []
            for i in range(len(foods)):
                food = Food.objects.get(food_no=foods[i])
                json = {
                    # "is_written": is_written[i],
                    "food_name": food.food_name,
                    "food_star": food.food_star,
                    "food_dsc": food.food_dsc,
                    # "food_class_no": food.food_class_no.food_class_no
                }
                eaten_food.append(json)

            return JsonResponse(eaten_food, safe=False, status=200)

    except KeyError:
        return JsonResponse({"message": "INVALID_KEY"}, status=400)
