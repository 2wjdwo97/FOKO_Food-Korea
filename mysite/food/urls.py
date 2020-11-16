from django.urls import path
from food import views

urlpatterns = [
    path('get/reviewed/', views.get_by_review_num),
]
