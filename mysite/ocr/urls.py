from django.urls import path
from ocr import views

urlpatterns = [
    path('', views.imageupload),
]
