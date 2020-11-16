import re
from soynlp.hangle import jamo_levenshtein
from multipledispatch import dispatch


def getTextResemblance(text1, text2):
    cost = {('ㅡ', 'ㅜ'): 0.4, ('ㅈ', 'ㅊ'): 0.4, ('ㅗ', 'ㅜ'): 0.4, \
            ('ㅁ', 'ㅇ'): 0.3, ('ㄹ', 'ㅌ'): 0.3, ('ㅗ', 'ㅛ'): 0.3, ('ㅏ', 'ㅣ'): 0.3}
    if len(text1) > len(text2):
        divider = len(text1)
    else:
        divider = len(text2)
    return 1 - jamo_levenshtein(text1, text2, cost) / divider


def preprocessText(input_text):
    output_list = []
    output_text = ''.join(i for i in re.sub(r" ?\([^)]+\)", "", input_text.replace(',', '')) if not i.isdigit())
    output_text = output_text.split('\n')

    for index, texts in enumerate(output_text):
        if texts:
            temp = [text for text in texts.split(' ') if text != '']
            if len(temp) == 1:
                temp = temp[0]
            output_list.append(temp)
    return output_list


@dispatch(str,list, float)
def getSimilarTextInBaseList(input_text, base_list, ratio_limit):
    cur_ratio = ratio_limit
    cur_text = None
    boundary = [int(ratio_limit * len(input_text)), int(1 / ratio_limit * len(input_text))]
    for base in base_list:
        if boundary[0] <= len(base) <= boundary[1]:
            new_ratio = getTextResemblance(input_text, base)
            if new_ratio > cur_ratio:
                cur_ratio = new_ratio
                cur_text = base
    return [cur_text]


@dispatch(list, list, float)
def getSimilarTextInBaseList(input_texts, base_list, ratio_limit):
    food_list = []
    start_idx = 0

    while start_idx < len(input_texts):
        compare_list = base_list
        temp_food = None
        temp_idx = start_idx + 1
        ratio_list = []

        for end_idx in range(start_idx, len(input_texts)):
            word = ''.join(input_texts[start_idx:end_idx + 1])
            crop_end = len(word)
            crop_start = crop_end - len(input_texts[end_idx])
            compare_list, ratio_list = getFoodList(word, compare_list, crop_start, crop_end, 0.6)

            if len(compare_list) == 0:
                break

            cur_ratio = ratio_limit
            for idx, food in enumerate(compare_list):
                if len(food) == len(word) and ratio_list[idx] >= cur_ratio:
                    temp_food = food
                    temp_idx = end_idx + 1
                    cur_ratio = ratio_list[idx]

        if temp_food:
            food_list.append(temp_food)
        start_idx = temp_idx

    return food_list


def getFoodList(word, base_list, start_idx, end_idx, ratio_limit):
    output_list = []
    ratio_list = []

    for food in base_list:
        # calculate resemblance between last text and substring of the food
        ratio = getTextResemblance(word[start_idx:], food[start_idx:end_idx])

        # if similar then add that food to a list
        # calculate resemblance between input text and string of the food
        if ratio >= ratio_limit:
            output_list.append(food)
            ratio_list.append(getTextResemblance(word, food))

    return output_list, ratio_list


def matchStr(input_string, base_list, ratio_limit = 0.7):
    match_list = []
    input_list = preprocessText(input_string)
    # match
    for input_text in input_list:
        results = getSimilarTextInBaseList(input_text, base_list, ratio_limit)
        for result in results:
            if result and result not in match_list:
                match_list.append(result)

    return match_list
