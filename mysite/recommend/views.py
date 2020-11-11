import numpy as np
# from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from food.models import Food, Ingredient, MapFoodIngre
from user.models import User, MapUserAllergy, MapUserFoodClass
from review.models import Review, MapFoodTag, MapUserTag

SELECTED_TAGS_RATIO = 0.1


@csrf_exempt
def recommend_ocr(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            user_no = data['user_no']

            foods = data['food_no']             # 음식
            foods_score = np.zeros(len(foods))  # 음식별 점수

            # 사용자 알레르기 찾기
            user_allergies = MapUserAllergy.objects.filter(user_no=user_no).values_list('allergy_no', flat=True)
            user_allergies = np.array(user_allergies)

            # 음식 알레르기 찾기
            food_allergies = []
            for i in range(len(foods)):
                food_no = foods[i]

                # MapFoodIngre.objects.filter(food_no=food_no).select_related('ingre_no').exclude(allergy_no=0).values_list('allergy_no', flat=True)
                ingredients = MapFoodIngre.objects.filter(food_no=food_no).values_list('ingre_no', flat=True)

                allergies = []
                for j in range(len(ingredients)):
                    allergy_no = Ingredient.objects.get(ingre_no=ingredients[j]).allergy_no.allergy_no
                    if allergy_no != 0:
                        allergies.append(allergy_no)

                food_allergies.append(np.unique(allergies))

            # 사용자 알레르기, 음식 알레르기 비교 후 같으면 점수 -1
            for i in range(len(food_allergies)):
                if np.intersect1d(food_allergies[i], user_allergies):
                    foods_score[i] = -1

            # 음식 점수 계산
            for i in range(len(foods)):
                if foods_score[i] == -1:
                    continue

                # 음식의 태그 찾기
                food_no = foods[i]
                food_tag_qs = MapFoodTag.objects.filter(food_no=food_no)                    # 후기에 작성된 음식의 태그 QuerySet
                obj_tag = [Food.objects.get(food_no=food_no).food_class_no.food_class_no]   # 음식의 객관적 태그
                subj_tags = np.unique(food_tag_qs.values_list('tag_no', flat=True))         # 음식의 주관적 태그
                food_tags = np.concatenate((obj_tag, subj_tags), axis=0)                    # 주관적 + 객관적

                selected_tag_ratio = round(food_tag_qs.count() * SELECTED_TAGS_RATIO)       # 사용자 선택 태그 반영 비율
                len_food_tag = len(food_tags)

                tags_score = np.zeros(len_food_tag)   # 음식 태그별 점수
                tags_weight = np.zeros(len_food_tag)  # 음식 태그별 가중치

                # 음식의 객관적 태그와 사용자가 선택한 객관적 태그 비교
                user_obj_tags = MapUserFoodClass.objects.filter(user_no=user_no).values_list('food_class_no', flat=True)
                if food_tags[0] in user_obj_tags:
                    tags_score[0] = 4.5
                    tags_weight[0] = selected_tag_ratio

                # 음식의 태그와 자신의 태그 비교
                user_review = Review.objects.filter(user_no=user_no).values_list('rev_no', flat=True)

                # weight 계산 (태그 개수)
                for j in range(1, len_food_tag):
                    tags_weight[j] = food_tag_qs.filter(tag_no=food_tags[j]).count()

                    # 1. 음식의 주관적 태그와 자신이 작성한 후기에서 포함된 주관적 태그 비교
                    star, cnt = 0, 0
                    for k in range(len(user_review)):
                        rev_no = MapFoodTag.objects.filter(rev_no=user_review[k]).filter(tag_no=food_tags[j])

                        if rev_no.exists():
                            rev_no = rev_no.values_list('rev_no', flat=True)[0]
                            star += int(Review.objects.get(rev_no=rev_no).rev_star)
                            cnt += 1

                    if cnt != 0:
                        star = round(star/cnt, 2)
                        tags_score[j] = star

                    # 2. 음식의 주관적 태그와 사용자가 선택한 주관적 태그 비교
                    if MapUserTag.objects.filter(user_no=user_no).filter(tag_no=food_tags[j]).values_list('tag_no', flat=True):
                        tags_score[j] = round((tags_score[j] + (4.5 * selected_tag_ratio)) / (cnt + selected_tag_ratio), 2)

                # print(tags_score)
                # print(tags_weight)

                # 총 점수 계산
                sum_score, sum_cnt = 0, 0
                for j in range(len_food_tag):
                    if tags_score[j] != 0:
                        sum_score += tags_score[j] * tags_weight[j]
                        sum_cnt += tags_weight[j]

                if sum_cnt != 0:
                    foods_score[i] = sum_score / sum_cnt

            idx_sorted_score = np.argsort(-foods_score)
            foods = np.array(foods)[idx_sorted_score]
            # print(foods_score)
            # print(foods)

            return JsonResponse({"message": "SUCCESS", "foods": foods.tolist()}, status=200)

        except KeyError as ke:
            print(ke)
            return JsonResponse({"message": "INVALID_KEYS"}, status=400)
