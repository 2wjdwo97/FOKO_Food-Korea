from django.db import models
from foods.models import Ingredients, Tags


class Countries(models.Model):
    country_no = models.AutoField(primary_key=True)
    country_ko_name = models.CharField(max_length=50)
    country_en_name = models.CharField(max_length=50)

    class Meta:
        db_table = 'data_countries'


class Users(models.Model):
    user_no = models.AutoField(primary_key=True)
    country_no = models.ForeignKey(Countries, on_delete=models.CASCADE)
    user_id = models.CharField(unique=True, max_length=20)
    user_pw = models.CharField(max_length=100)
    user_name = models.CharField(max_length=50)
    user_age = models.PositiveSmallIntegerField()
    user_spicy = models.PositiveSmallIntegerField()

    class Meta:
        db_table = 'data_users'


class MapUserIngre(models.Model):
    user_no = models.ForeignKey(Users, on_delete=models.CASCADE)
    ingre_no = models.ForeignKey(Ingredients, on_delete=models.CASCADE)

    class Meta:
        db_table = 'map_user_ingre'


class MapUserTag(models.Model):
    user_no = models.ForeignKey(Users, on_delete=models.CASCADE)
    tag_no = models.ForeignKey(Tags, on_delete=models.CASCADE)

    class Meta:
        db_table = 'map_user_tag'
