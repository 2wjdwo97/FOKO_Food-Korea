from django.urls import path
from food import views

urlpatterns = [
    path('get/order/review/', views.get_most_reviewed),
    path('get/order/star/', views.get_highest_rated),
]
