from django.db import models


class Classes(models.Model):
    class_no = models.IntegerField(primary_key=True)
    class_ko_name = models.CharField(max_length=50)
    class_en_name = models.CharField(max_length=50)

    class Meta:
        db_table = 'data_classes'


class Countries(models.Model):
    country_no = models.AutoField(primary_key=True)
    country_ko_name = models.CharField(max_length=50)
    country_en_name = models.CharField(max_length=50)

    class Meta:
        db_table = 'data_countries'


class Foods(models.Model):
    food_no = models.AutoField(primary_key=True)
    class_no = models.ForeignKey(Classes, on_delete=models.CASCADE)
    food_name = models.CharField(unique=True, max_length=50)
    food_dsc = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'data_foods'


class Ingredients(models.Model):
    ingre_no = models.AutoField(primary_key=True)
    ingre_name = models.CharField(max_length=50)
    ingre_en_name = models.CharField(max_length=50, blank=True, null=True)
    ingre_allergy = models.BooleanField()

    class Meta:
        db_table = 'data_ingredients'


class Tags(models.Model):
    tag_no = models.IntegerField(primary_key=True)
    tag_name = models.CharField(max_length=50)

    class Meta:
        db_table = 'data_tags'


class MapFoodIngre(models.Model):
    food_no = models.ForeignKey(Foods, models.DO_NOTHING, db_column='food_no')
    ingre_no = models.ForeignKey(Ingredients, models.DO_NOTHING, db_column='ingre_no')

    class Meta:
        db_table = 'map_food_ingre'


class MapFoodTag(models.Model):
    food_no = models.ForeignKey(Foods, models.DO_NOTHING, db_column='food_no')
    tag_no = models.ForeignKey(Tags, models.DO_NOTHING, db_column='tag_no')

    class Meta:
        db_table = 'map_food_tag'
