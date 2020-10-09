from rest_framework import serializers
from django.contrib.auth import get_user_model


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        User = get_user_model()
        model = User
        fields = ['user_id', 'user_pw', 'user_age', 'user_country']
