from django.urls import path
from OCR import views

urlpatterns = [
    path('', views.imageUpload),
]
