from rest_framework import serializers

from .models import Review, MapFoodTag


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['user_no', 'food_no', 'rev_star', 'rev_spicy', 'rev_contents']


class MapFoodUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapFoodTag
        fields = ['rev_no', 'food_no', 'tag_no']

# {
#     "user_no": 3,
#     "food_no": 6,
#     "rev_star": 3,
#     "rev_spicy": 1,
#     "rev_contents": "yummy",
#     "tag_no": [5, 6, 23]
# }