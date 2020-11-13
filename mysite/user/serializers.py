from rest_framework import serializers

from .models import Country, User


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['country_no', 'country_ko_name', 'country_en_name']


class UserSerializer(serializers.ModelSerializer):
    # country_no = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = User
        fields = ['user_id',
                  'user_pw',
                  'user_email',
                  'user_name',
                  'user_birth',
                  'user_spicy',
                  'country_no']

# 회원가입
# {
# 	"user_id" : "pkm1015",
# 	"user_pw" : "1015pkm",
# 	"pw_confirm" : "1015pkm",
# 	"user_email" : "kio971015@gmail.com",
# 	"user_name" : "park",
# 	"user_birth" : "1997-10-15",
# 	"user_spicy" : 4,
# 	"country_no" : 37
# }
# 개인 설정
# {
#    "user_no" : 11,
#    "food_class_no" : [16, 27],
#    "tag_no" : [1, 6, 17, 31],
#    "allergy_no" : [6, 18]
# }
# 개인 설정 변경
# {
#    "user_no" : 1,
# 	 "user_spicy" : 1,
# 	 "country_no" : 1,
#    "food_class_no" : [16, 27],
#    "tag_no" : [1, 6, 17, 31],
#    "allergy_no" : [6, 18]
# }
# 비밀번호 변경
# {
# 	"user_no": 1,
# 	"user_pw": "1015pkm",
#   "pw_new": "971015pkm",
# 	"pw_confirm": "971015pkm"
# }