import re


def splitKor(string):
    BASE_CODE, CHOSUNG, JUNGSUNG = 44032, 588, 28
    CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
    JUNGSUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
    JONGSUNG_LIST = ['', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

    sp_list = list(string)
    result = []
    for keyword in sp_list:
        if re.match('.*[가-힣]+.*', keyword):
            char_code = ord(keyword) - BASE_CODE
            char1 = int(char_code / CHOSUNG)
            result.append(CHOSUNG_LIST[char1])

            char2 = int((char_code - (CHOSUNG * char1)) / JUNGSUNG)
            result.append(JUNGSUNG_LIST[char2])

            char3 = int(char_code - (CHOSUNG * char1) - (JUNGSUNG * char2))
            if char3 != 0:
                result.append(JONGSUNG_LIST[char3])
        else:
            result.append(keyword)
    return "".join(result)



def getShingle(text, unitSize, temp=-1):
    strPieces = splitKor(text)
    shingle = []

    # create shingle
    for i in range(len(strPieces) - (unitSize - 1)):
        shingle.append(strPieces[i:i+unitSize])

    temp = set(shingle)
    return temp


def getTextResemblance(set1, set2):
    return len(set1 & set2) / len(set1 | set2)


def getTheMostSimilarText(input_list, base_list, ratioLimit=0.5, unitSize=2):
    shingle_base = []
    shingle_input = []
    match_list = []

    # create base_list shingle
    for text in base_list:
        shingle_base.append(getShingle(text, unitSize))

    # create input_list shingle
    for i, text in enumerate(input_list):
        shingle_input.append(getShingle(text, unitSize, i))

    # match
    for num, input in enumerate(shingle_input):
        curRatio = 0
        curText = None

        for index, base in enumerate(shingle_base):
            newRatio = getTextResemblance(input, base)
            if newRatio > curRatio:
                curRatio = newRatio
                curText = base_list[index]

        # append curText to match_list when the curRatio is greater or equal to limit
        if curRatio >= ratioLimit and curText not in match_list:
            match_list.append(curText)

    return match_list
