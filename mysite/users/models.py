from django.db import models

from foods.models import Classes, AllergyClasses

DEGREE = (('1', 'very bad'), ('2', 'bad'), ('3', 'so so'), ('4', 'good'), ('5', 'very good'))


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
    user_spicy = models.CharField(max_length=1, choices=DEGREE)

    class Meta:
        db_table = 'data_users'


class MapUserClass(models.Model):
    user_no = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='user_no')
    food_class_no = models.ForeignKey(Classes, on_delete=models.CASCADE, db_column='food_class_no')

    class Meta:
        db_table = 'map_user_class'


class MapUserAllergy(models.Model):
    user_no = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='user_no')
    allergy_no = models.ForeignKey(AllergyClasses, on_delete=models.CASCADE, db_column='allergy_no')

    class Meta:
        db_table = 'map_user_allergy'
