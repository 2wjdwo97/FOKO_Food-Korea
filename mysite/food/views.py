import numpy as np

from datetime import datetime
from django.http import JsonResponse
from django.utils.dateformat import DateFormat
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from ocr import googleCloudService
from review.models import MapFoodTag, Review
from .models import Food, MapFoodIngre, Ingredient

match_btn_foodclass = {
    1: [1, 2],            # 밥/김밥/초밥류
    2: [3, 13, 14, 15],   # 죽/스프/국탕/찌개/전골류
    3: [4],               # 면/만두류
    4: [18],              # 볶음류
    5: [9, 20],           # 튀김류
    6: [17],              # 구이류
    7: [6, 7, 8, 9, 10],  # 빵/버거/피자/샌드위치류
    8: [19],              # 조림류
    9: [16],              # 찜류
    10: [12]              # 음료/차류
}
TODAY_FOOD_CNT = 5


@csrf_exempt
def get_today_special(request):
    if request.method == 'GET':
        try:
            # 오늘 날짜 구하기
            today = str(DateFormat(datetime.now()).format('Ymd'))
            year, month, day = today[0:4], today[4:6], today[6:8]
            start_date = datetime.strptime(year + " " + month + " " + day, '%Y %m %d')
            end_date = datetime.strptime(year + " " + month + " " + day + " 23:59", '%Y %m %d %H:%M')

            # 하루 중 평균 별점이 높은 음식 5가지 구하기
            today = Review.objects.filter(rev_date__range=[start_date, end_date])
            if today.exists():
                foods = today.distinct().values_list('food_no', flat=True)

                # 음식별 오늘의 평균 별점 구하기
                review_star = np.array([])
                for food_no in foods:
                    food_review = today.filter(food_no=food_no)
                    food_star = food_review.values_list('rev_star', flat=True)
                    sum_star = sum(food_star)
                    review_star = np.append(review_star, [sum_star / food_review.count()])

                # 별점 높은 순으로 정렬
                sorted_star = np.sort(review_star)[::-1]
                idx_sorted_cnt = np.argsort(-review_star)
                foods = np.array(foods)[idx_sorted_cnt]

                # 5가지 음식만 추출
                if len(foods) > TODAY_FOOD_CNT:
                    foods = foods[:TODAY_FOOD_CNT]
                    sorted_star = sorted_star[:TODAY_FOOD_CNT]

                request = get_foods_by_list(foods)
                for i in range(len(request)):
                    request[i]["today_avg_star"] = sorted_star[i]

                return JsonResponse(request, safe=False, status=200)    # 정상
            return JsonResponse(request, safe=False, status=201)        # 하루동안 작성된 리뷰가 없는 경우
        except KeyError:
            return JsonResponse({"message": "INVALID_KEY"}, status=400)


@csrf_exempt
def get_most_reviewed(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            button_no = data['button_no']

            foods = Food.objects.none()
            for food_class_no in match_btn_foodclass[button_no]:
                foods = foods | Food.objects.filter(food_class_no=food_class_no)

            foods = foods.order_by('-food_review_count')

            return JsonResponse(get_foods_by_queryset(foods), safe=False, status=200)

        except KeyError:
            return JsonResponse({"message": "INVALID_KEY"}, status=400)


@csrf_exempt
def get_highest_rated(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            button_no = data['button_no']

            foods = Food.objects.none()
            for food_class_no in match_btn_foodclass[button_no]:
                foods = foods | Food.objects.filter(food_class_no=food_class_no)

            foods = foods.order_by('-food_star')

            return JsonResponse(get_foods_by_queryset(foods), safe=False, status=200)

        except KeyError:
            return JsonResponse({"message": "INVALID_KEY"}, status=400)


def get_foods_by_queryset(foods):
    data_foods = []
    for food in foods:
        tags = calc_tags(food.food_no)
        allergies = calc_allergys(food.food_no)

        data = {
            "food_name": food.food_name,
            "translated_name": googleCloudService.translate(food.food_name),
            "food_star": food.food_star,
            "food_review_count": food.food_review_count,
            "food_dsc": food.food_dsc,
            "food_img_url": food.food_img_url,
            "tag_no": tags,
            "allergy": allergies
        }
        data_foods.append(data)

    return data_foods


def get_foods_by_list(foods):
    data_foods = []
    for food_no in foods:
        tags = calc_tags(food_no)
        allergies = calc_allergys(food_no)

        food = Food.objects.get(food_no=food_no)
        data = {
            "food_name": food.food_name,
            "translated_name": googleCloudService.translate(food.food_name),
            "food_star": food.food_star,
            "food_spicy": food.food_spicy,
            "food_review_count": food.food_review_count,
            "food_dsc": food.food_dsc,
            "food_img_url": food.food_img_url,
            "tag_no": tags,
            "allergy": allergies
        }
        data_foods.append(data)

    return data_foods


def calc_allergys(food_no):
    allergies = []
    ingredients = MapFoodIngre.objects.filter(food_no=food_no).values_list('ingre_no', flat=True)

    for ingredient in ingredients:
        # 음식에 포함된 식재료
        # ingre_en_name = Ingredient.objects.get(ingre_no=ingredient).ingre_en_name
        # ingredient_names.append(ingre_en_name)

        # 음식에 포함된 알레르기 정보
        allergy = googleCloudService.translate(Ingredient.objects.get(ingre_no=ingredient).allergy_no.allery_en_name)
        if allergy != 0 and allergy not in allergies:
            allergies.append(allergy)

    return allergies


# 음식에 포함된 태그(3가지) 리턴
def calc_tags(food_no):
    # 객관적 태그
    tags = [Food.objects.get(food_no=food_no).food_class_no.food_class_no]

    # 주관적 태그
    food_tags_qs = MapFoodTag.objects.filter(food_no=food_no)
    if food_tags_qs.exists():
        subj_tags = np.unique(food_tags_qs.values_list('tag_no', flat=True))
        subj_tags_cnt = np.array(subj_tags)
        for subj_tag in subj_tags:
            np.append(subj_tags_cnt, food_tags_qs.filter(tag_no=subj_tag).count())

        idx_sorted_cnt = np.argsort(-subj_tags_cnt)
        subj_tags = np.array(subj_tags)[idx_sorted_cnt]

        for i in range(len(subj_tags)):
            if i > 1:
                break
            np.append(tags, subj_tags[i])

    return tags
