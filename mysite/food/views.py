import numpy as np

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from review.models import Tag, MapFoodTag
from .models import Food, MapFoodIngre, Ingredient, FoodClass, AllergyClass
from .serializers import FoodSerializer


@csrf_exempt
def get_by_review_num(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            food_class_no = data['food_class_no']

            if food_class_no == 1:
                foods = Food.objects.filter(food_class_no=1) | Food.objects.filter(food_class_no=2)
            elif food_class_no == 2:
                foods = Food.objects.filter(food_class_no=3) | Food.objects.filter(food_class_no=13) | Food.objects.filter(food_class_no=14) | Food.objects.filter(food_class_no=15)
            elif food_class_no == 3:
                foods = Food.objects.filter(food_class_no=4)
            elif food_class_no == 4:
                foods = Food.objects.filter(food_class_no=18)
            elif food_class_no == 5:
                foods = Food.objects.filter(food_class_no=9) | Food.objects.filter(food_class_no=20)
            elif food_class_no == 6:
                foods = Food.objects.filter(food_class_no=17)
            elif food_class_no == 7:
                foods = Food.objects.filter(food_class_no=6) | Food.objects.filter(food_class_no=7) | Food.objects.filter(food_class_no=8) | Food.objects.filter(food_class_no=9) | Food.objects.filter(food_class_no=10)
            elif food_class_no == 8:
                foods = Food.objects.filter(food_class_no=19)
            elif food_class_no == 9:
                foods = Food.objects.filter(food_class_no=16)
            elif food_class_no == 10:
                foods = Food.objects.filter(food_class_no=12)

            foods = foods.order_by('-food_review_count')

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
            "food_star": food.food_star,
            "food_review_count": food.food_review_count,
            "food_dsc": food.food_dsc,
            "tag_no": tags,
            "allergy_no": allergies
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
            "food_star": food.food_star,
            "food_review_count": food.food_review_count,
            "food_dsc": food.food_dsc,
            "tag_no": tags,
            "allergy_no": allergies
        }
        data_foods.append(data)

    return data_foods


def calc_tags(food_no):
    allergies = []
    ingredients = MapFoodIngre.objects.filter(food_no=food_no).values_list('ingre_no', flat=True)

    for ingredient in ingredients:
        # 음식에 포함된 식재료
        # ingre_en_name = Ingredient.objects.get(ingre_no=ingredient).ingre_en_name
        # ingredient_names.append(ingre_en_name)

        # 음식에 포함된 알레르기 정보
        allergy = Ingredient.objects.get(ingre_no=ingredient).allergy_no.allergy_no
        if allergy != 0 and allergy not in allergies:
            allergies.append(allergy)

    return allergies


def calc_allergys(food_no):
    # 음식에 포함된 태그(3가지) 리턴
    # 객관적 태그 추가
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
