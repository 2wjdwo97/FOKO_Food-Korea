from rest_framework import serializers
from .models import Foods


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Foods
        fields = ['food_no', 'class_no', 'food_name', 'food_dsc']
