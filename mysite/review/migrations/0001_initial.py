# Generated by Django 3.1.1 on 2020-11-11 15:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
        ('food', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('tag_no', models.IntegerField(primary_key=True, serialize=False)),
                ('tag_ko_name', models.CharField(max_length=50)),
                ('tag_en_name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'data_tags',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('rev_no', models.AutoField(db_column='rev_no', primary_key=True, serialize=False)),
                ('rev_date', models.DateTimeField(auto_now_add=True)),
                ('rev_star', models.CharField(choices=[('1', 'very bad'), ('2', 'bad'), ('3', 'so so'), ('4', 'good'), ('5', 'very good')], max_length=1)),
                ('rev_spicy', models.CharField(choices=[('1', 'very bad'), ('2', 'bad'), ('3', 'so so'), ('4', 'good'), ('5', 'very good')], max_length=1)),
                ('rev_contents', models.TextField(null=True)),
                ('food_no', models.ForeignKey(db_column='food_no', on_delete=django.db.models.deletion.CASCADE, to='food.food')),
                ('user_no', models.ForeignKey(db_column='user_no', on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
            options={
                'db_table': 'data_reviews',
            },
        ),
        migrations.CreateModel(
            name='MapUserTag',
            fields=[
                ('id', models.AutoField(db_column='id', primary_key=True, serialize=False)),
                ('tag_no', models.ForeignKey(db_column='tag_no', on_delete=django.db.models.deletion.CASCADE, to='review.tag')),
                ('user_no', models.ForeignKey(db_column='user_no', on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
            options={
                'db_table': 'map_user_tag',
            },
        ),
        migrations.CreateModel(
            name='MapFoodTag',
            fields=[
                ('id', models.AutoField(db_column='id', primary_key=True, serialize=False)),
                ('food_no', models.ForeignKey(db_column='food_no', on_delete=django.db.models.deletion.CASCADE, to='food.food')),
                ('rev_no', models.ForeignKey(db_column='rev_no', on_delete=django.db.models.deletion.CASCADE, to='review.review')),
                ('tag_no', models.ForeignKey(db_column='tag_no', on_delete=django.db.models.deletion.CASCADE, to='review.tag')),
            ],
            options={
                'db_table': 'map_food_tag',
            },
        ),
    ]
