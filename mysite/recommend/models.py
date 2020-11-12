from django.db import models

from food.models import Food
from user.models import Country


class FoodRankCountry(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    food_no = models.ForeignKey(Food, on_delete=models.CASCADE, db_column='food_no')
    country_no = models.ForeignKey(Country, on_delete=models.CASCADE, db_column='country_no')
    rank = models.PositiveSmallIntegerField()

    class Meta:
        db_table = 'data_food_rank_country'


class FoodRankAge(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    food_no = models.ForeignKey(Food, on_delete=models.CASCADE, db_column='food_no')
    age = models.PositiveSmallIntegerField()
    rank = models.PositiveSmallIntegerField()

    class Meta:
        db_table = 'data_food_rank_age'
