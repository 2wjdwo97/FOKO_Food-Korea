from django.db import models
from django.conf import settings
from django.utils import timezone

from food.models import Food, FoodClass, AllergyClass


class Country(models.Model):
    country_no = models.AutoField(primary_key=True)
    country_ko_name = models.CharField(max_length=50)
    country_en_name = models.CharField(max_length=50)

    class Meta:
        db_table = 'data_countries'


class Language(models.Model):
    lang_no = models.AutoField(primary_key=True)
    lang_en_name = models.CharField(max_length=20)
    lang_code = models.CharField(max_length=5)

    class Meta:
        db_table = 'data_languages'


class User(models.Model):
    user_no = models.AutoField(primary_key=True)
    user_id = models.CharField(unique=True, max_length=20)
    user_pw = models.CharField(max_length=128)
    user_email = models.EmailField(unique=True)

    user_name = models.CharField(max_length=50)
    user_birth = models.DateField(null=True, blank=True)
    user_spicy = models.FloatField(default=0)

    country_no = models.ForeignKey(Country, on_delete=models.CASCADE, db_column='country_no')
    lang_no = models.ForeignKey(Language, default=8, on_delete=models.CASCADE, db_column='lang_no')

    is_active = models.BooleanField(default=False)
    is_first = models.BooleanField(default=True)

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['user_name', 'user_birth', 'user_spicy', 'country_no']

    class Meta:
        db_table = 'data_users'


class MapUserFoodClass(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    user_no = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_no')
    food_class_no = models.ForeignKey(FoodClass, on_delete=models.CASCADE, db_column='food_class_no')

    class Meta:
        db_table = 'map_user_food_class'


class MapUserAllergy(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    user_no = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_no')
    allergy_no = models.ForeignKey(AllergyClass, on_delete=models.CASCADE, db_column='allergy_no')

    class Meta:
        db_table = 'map_user_allergy'


class MapUserEat(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    user_no = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_no')
    food_no = models.ForeignKey(Food, on_delete=models.CASCADE, db_column='food_no')
    is_written = models.BooleanField(default=False)

    class Meta:
        db_table = 'map_user_eat'


# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
#
# class UserManager(BaseUserManager):
#     use_in_migrations = True
#
#     # user 생성 함수
#     def _create_user(self, user_id, password, **kwargs):
#         if not user_id:
#             raise ValueError('must have user id')
#         kwargs['country_no'] = Country.objects.get(country_no=kwargs.get('country_no'))
#         user = self.model(user_id=user_id, **kwargs)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     # user 생성
#     def create_user(self, user_id, password=None, **kwargs):
#         kwargs.setdefault('is_superuser', False)
#         return self._create_user(user_id, password, **kwargs)
#
#     # admin 생성
#     def create_superuser(self, user_id, password, **kwargs):
#         kwargs.setdefault('is_superuser', True)
#         if kwargs.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')
#         return self._create_user(user_id, password, **kwargs)
#
#
# class User(AbstractBaseUser, PermissionsMixin):
#     user_no = models.AutoField(primary_key=True, unique=True, verbose_name='No.')
#     user_id = models.CharField(unique=True, max_length=20, verbose_name='User id')
#     user_name = models.CharField(max_length=50, verbose_name='User name')
#     user_age = models.PositiveSmallIntegerField(verbose_name='Age')
#     user_spicy = models.CharField(max_length=1, choices=DEGREE, verbose_name='Spicy')
#     country_no = models.ForeignKey(Country, on_delete=models.CASCADE, db_column='country_no', verbose_name='Country no.')
#     password = models.CharField(max_length=128)
#
#     is_active = models.BooleanField(default=True)
#     is_superuser = models.BooleanField(default=False)
#
#     objects = UserManager()
#
#     USERNAME_FIELD = 'user_id'
#     REQUIRED_FIELDS = ['user_name', 'user_age', 'user_spicy', 'country_no']
#
#     class Meta:
#         db_table = 'auth_users'
