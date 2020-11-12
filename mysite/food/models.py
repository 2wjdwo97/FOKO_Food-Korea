from django.db import models


class FoodClass(models.Model):
    food_class_no = models.IntegerField(primary_key=True)
    food_class_ko_name = models.CharField(max_length=50)
    food_class_en_name = models.CharField(max_length=50)

    class Meta:
        db_table = 'data_food_classes'


class AllergyClass(models.Model):
    allergy_no = models.IntegerField(primary_key=True)
    allergy_ko_name = models.CharField(max_length=50)
    allergy_en_name = models.CharField(max_length=50)

    class Meta:
        db_table = 'data_allergy_classes'


class Food(models.Model):
    food_no = models.AutoField(primary_key=True)
    food_class_no = models.ForeignKey(FoodClass, on_delete=models.CASCADE, db_column='food_class_no')
    food_name = models.CharField(max_length=50)
    food_dsc = models.TextField(null=True)
    food_img = models.ImageField(null=True)
    food_star = models.SmallIntegerField(default=0)
    food_review_count = models.IntegerField(default=0)

    class Meta:
        db_table = 'data_foods'


class Ingredient(models.Model):
    ingre_no = models.AutoField(primary_key=True)
    ingre_ko_name = models.CharField(max_length=50)
    ingre_en_name = models.CharField(max_length=50, null=True)
    allergy_no = models.ForeignKey(AllergyClass, on_delete=models.CASCADE, db_column='allergy_no')

    class Meta:
        db_table = 'data_ingredients'


class MapFoodIngre(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    food_no = models.ForeignKey(Food, on_delete=models.CASCADE, db_column='food_no')
    ingre_no = models.ForeignKey(Ingredient, on_delete=models.CASCADE, db_column='ingre_no')

    class Meta:
        db_table = 'map_food_ingre'


class MapFoodIngreAdd(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    food_no = models.ForeignKey(Food, on_delete=models.CASCADE, db_column='food_no')
    ingre_no = models.ForeignKey(Ingredient, on_delete=models.CASCADE, db_column='ingre_no')

    class Meta:
        db_table = 'map_food_ingre_add'
