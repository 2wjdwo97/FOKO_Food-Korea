from django.db import models

from foods.models import Foods
from users.models import Users, DEGREE


class Reviews(models.Model):
    user_no = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='user_no')
    food_no = models.ForeignKey(Foods, on_delete=models.CASCADE, db_column='food_no')
    rev_data = models.DateTimeField(auto_now_add=True)
    rev_star = models.CharField(max_length=1, choices=DEGREE)
    rev_spicy = models.CharField(max_length=1, choices=DEGREE)
    rev_contents = models.TextField(null=True)
    rev_manual = models.TextField(null=True)

    class Meta:
        db_table = 'data_reviews'


class Tags(models.Model):
    tag_no = models.IntegerField(primary_key=True)
    tag_ko_name = models.CharField(max_length=50)
    tag_en_name = models.CharField(max_length=50)

    class Meta:
        db_table = 'data_tags'


class MapFoodTag(models.Model):
    food_no = models.ForeignKey(Foods, on_delete=models.CASCADE, db_column='food_no')
    tag_no = models.ForeignKey(Tags, on_delete=models.CASCADE, db_column='tag_no')
    tag_cnt = models.IntegerField()

    class Meta:
        db_table = 'map_food_tag'


class MapUserTag(models.Model):
    user_no = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='user_no')
    tag_no = models.ForeignKey(Tags, on_delete=models.CASCADE, db_column='tag_no')

    class Meta:
        db_table = 'map_user_tag'

