from django.db import models


class Classes(models.Model):
    class_no = models.IntegerField(primary_key=True)
    class_ko_name = models.CharField(max_length=50)
    class_en_name = models.CharField(max_length=50)

    class Meta:
        db_table = 'data_classes'


class AllergyClasses(models.Model):
    allergy_no = models.IntegerField(primary_key=True)
    allergy_ko_name = models.CharField(max_length=50)
    allergy_en_name = models.CharField(max_length=50)

    class Meta:
        db_table = 'data_allergy_classes'


class Foods(models.Model):
    food_no = models.AutoField(primary_key=True)
    class_no = models.ForeignKey(Classes, on_delete=models.CASCADE)
    food_name = models.CharField(max_length=50)
    food_dsc = models.TextField(null=True)

    class Meta:
        db_table = 'data_foods'


class Ingredients(models.Model):
    ingre_no = models.AutoField(primary_key=True)
    ingre_ko_name = models.CharField(max_length=50)
    ingre_en_name = models.CharField(max_length=50, null=True)
    allergy_no = models.ForeignKey(AllergyClasses, on_delete=models.CASCADE)

    class Meta:
        db_table = 'data_ingredients'


class MapFoodIngre(models.Model):
    food_no = models.ForeignKey(Foods, db_column='food_no', on_delete=models.CASCADE)
    ingre_no = models.ForeignKey(Ingredients, db_column='ingre_no', on_delete=models.CASCADE)

    class Meta:
        db_table = 'map_food_ingre'


class MapFoodIngreAdd(models.Model):
    food_no = models.ForeignKey(Foods, db_column='food_no', on_delete=models.CASCADE)
    ingre_no = models.ForeignKey(Ingredients, db_column='ingre_no', on_delete=models.CASCADE)

    class Meta:
        db_table = 'map_food_ingre_add'
