# Generated by Django 3.1.1 on 2020-10-23 15:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AllergyClass',
            fields=[
                ('allergy_no', models.IntegerField(primary_key=True, serialize=False)),
                ('allergy_ko_name', models.CharField(max_length=50)),
                ('allergy_en_name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'data_allergy_classes',
            },
        ),
        migrations.CreateModel(
            name='Food',
            fields=[
                ('food_no', models.AutoField(primary_key=True, serialize=False)),
                ('food_name', models.CharField(max_length=50)),
                ('food_dsc', models.TextField(null=True)),
            ],
            options={
                'db_table': 'data_foods',
            },
        ),
        migrations.CreateModel(
            name='FoodClass',
            fields=[
                ('food_class_no', models.IntegerField(primary_key=True, serialize=False)),
                ('food_class_ko_name', models.CharField(max_length=50)),
                ('food_class_en_name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'data_food_classes',
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('ingre_no', models.AutoField(primary_key=True, serialize=False)),
                ('ingre_ko_name', models.CharField(max_length=50)),
                ('ingre_en_name', models.CharField(max_length=50, null=True)),
                ('allergy_no', models.ForeignKey(db_column='allergy_no', on_delete=django.db.models.deletion.CASCADE, to='food.allergyclass')),
            ],
            options={
                'db_table': 'data_ingredients',
            },
        ),
        migrations.CreateModel(
            name='MapFoodIngreAdd',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_no', models.ForeignKey(db_column='food_no', on_delete=django.db.models.deletion.CASCADE, to='food.food')),
                ('ingre_no', models.ForeignKey(db_column='ingre_no', on_delete=django.db.models.deletion.CASCADE, to='food.ingredient')),
            ],
            options={
                'db_table': 'map_food_ingre_add',
            },
        ),
        migrations.CreateModel(
            name='MapFoodIngre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_no', models.ForeignKey(db_column='food_no', on_delete=django.db.models.deletion.CASCADE, to='food.food')),
                ('ingre_no', models.ForeignKey(db_column='ingre_no', on_delete=django.db.models.deletion.CASCADE, to='food.ingredient')),
            ],
            options={
                'db_table': 'map_food_ingre',
            },
        ),
        migrations.AddField(
            model_name='food',
            name='food_class_no',
            field=models.ForeignKey(db_column='food_class_no', on_delete=django.db.models.deletion.CASCADE, to='food.foodclass'),
        ),
    ]
