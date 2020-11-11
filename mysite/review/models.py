from django.db import models

from food.models import Food
from user.models import DEGREE, User


class Review(models.Model):
    rev_no = models.AutoField(primary_key=True, db_column='rev_no')
    user_no = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_no')
    food_no = models.ForeignKey(Food, on_delete=models.CASCADE, db_column='food_no')
    rev_date = models.DateTimeField(auto_now_add=True)
    rev_star = models.CharField(max_length=1, choices=DEGREE)
    rev_spicy = models.CharField(max_length=1, choices=DEGREE)
    rev_contents = models.TextField(null=True)

    class Meta:
        db_table = 'data_reviews'


class Tag(models.Model):
    tag_no = models.IntegerField(primary_key=True)
    tag_ko_name = models.CharField(max_length=50)
    tag_en_name = models.CharField(max_length=50)

    class Meta:
        db_table = 'data_tags'


class MapFoodTag(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    rev_no = models.ForeignKey(Review, on_delete=models.CASCADE, db_column='rev_no')
    food_no = models.ForeignKey(Food, on_delete=models.CASCADE, db_column='food_no')
    tag_no = models.ForeignKey(Tag, on_delete=models.CASCADE, db_column='tag_no')

    class Meta:
        db_table = 'map_food_tag'


class MapUserTag(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    user_no = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_no')
    tag_no = models.ForeignKey(Tag, on_delete=models.CASCADE, db_column='tag_no')

    class Meta:
        db_table = 'map_user_tag'
