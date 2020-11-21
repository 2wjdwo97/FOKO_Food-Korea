# Generated by Django 3.1.2 on 2020-11-21 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20201117_0255'),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('lang_no', models.AutoField(primary_key=True, serialize=False)),
                ('lang_en_name', models.CharField(max_length=20)),
                ('lang_code', models.CharField(max_length=5)),
            ],
            options={
                'db_table': 'data_languages',
            },
        ),
    ]
