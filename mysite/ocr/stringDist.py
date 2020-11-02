import re
from soynlp.hangle import levenshtein
from soynlp.hangle import decompose

def jamo_levenshtein(s1, s2, cost):
    if len(s1) < len(s2):
        return jamo_levenshtein(s2, s1, cost)

    if len(s2) == 0:
        return len(s1)

    def substitution_cost(c1, c2):
        if c1 == c2:
            return 0
        return levenshtein(decompose(c1), decompose(c2), cost) / 3

    previous_row = range(len(s2) + 1)

    for i, c1 in enumerate(s1):
        current_row = [i + 1]

        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + substitution_cost(c1, c2)

            current_row.append(min(insertions, deletions, substitutions))

        previous_row = current_row

    return previous_row[-1]


def getTextResemblance(text1, text2):
    cost = {('ㅡ', 'ㅜ'): 0.7, ('ㅈ', 'ㅊ'): 0.7, ('ㅏ', 'ㅣ'): 0.6, ('ㅗ', 'ㅜ'): 0.7, ('ㅁ', 'ㅇ'): 0.6}
    if len(text1) > len(text2):
        divider = len(text1)
    else:
        divider = len(text2)
    return 1 - jamo_levenshtein(text1, text2, cost) / divider


def removeUseless(text_list):
    output = []
    for index, text in enumerate(text_list):
        output_text = ''.join(i for i in re.sub(r" ?\([^)]+\)", "", text.replace(',', '')) if not i.isdigit())
        if output_text != '':
            output.append(output_text)

    return output


def matchStr(input_list, base_list, ratioLimit = 0.7):
    match_list = []
    # match
    for input in input_list:
        curRatio = 0
        curText = None
        boundary = [int(ratioLimit * len(input)), int(1 / ratioLimit * len(input))]

        for base in base_list:
            if boundary[0] <= len(base) <= boundary[1]:
                newRatio = getTextResemblance(input, base)
                if newRatio > curRatio:
                    curRatio = newRatio
                    curText = base

        # append curText to match_list when the curRatio is greater or equal to limit
        if curRatio >= ratioLimit and curText not in match_list:
            match_list.append(curText)

    return match_list
