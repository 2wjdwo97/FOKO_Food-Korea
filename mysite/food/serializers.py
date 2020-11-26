from rest_framework import serializers

from .models import Food


class GetFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ['food_name', 'food_dsc', 'food_star', 'food_spicy', 'food_review_count', 'food_img_url']
