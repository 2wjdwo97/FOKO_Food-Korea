# Generated by Django 3.1.2 on 2020-11-16 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='rev_spicy',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='review',
            name='rev_star',
            field=models.FloatField(default=0),
        ),
    ]
