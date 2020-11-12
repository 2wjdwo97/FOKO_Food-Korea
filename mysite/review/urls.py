from django.urls import path
from . import views

urlpatterns = [
    path('get_all/', views.get_all_review),
    path('get_user/', views.get_user_review),
    path('save/', views.save),
    path('eat/', views.get_eaten_food),
]