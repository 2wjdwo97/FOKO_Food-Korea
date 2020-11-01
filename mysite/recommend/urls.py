from django.urls import path
from . import views

urlpatterns = [
    path('ocr/', views.recommend_ocr),
]