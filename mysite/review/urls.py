from django.urls import path
from . import views

urlpatterns = [
    path('get_all/', views.get_all_review),
    path('get_user/', views.get_user_review),
    path('save/', views.save_review),
    path('eaten/get/', views.get_eaten_food),
    path('eaten/save/', views.save_eaten_food),
]