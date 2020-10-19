from rest_framework import serializers

from .models import Food


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ['food_no', 'class_no', 'food_name', 'food_dsc']
