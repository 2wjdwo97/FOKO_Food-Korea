from django.urls import path
from food import views

urlpatterns = [
    path('get/reviewed/', views.get_most_reviewed),
    path('get/rated/', views.get_highest_rated),
]
