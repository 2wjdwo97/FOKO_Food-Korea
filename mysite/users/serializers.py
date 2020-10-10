from rest_framework import serializers

from users.models import Users


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['user_id',
                  'user_pw',
                  'user_name',
                  'user_age',
                  'user_spicy',
                  'country_no']

# json example
# {
# 	"user_id" : "kio1015",
# 	"user_pw" : "pkm1015",
# 	"user_name" : "park",
# 	"user_age" : "24",
# 	"user_spicy" : "2",
# 	"country_no" : "10"
# }