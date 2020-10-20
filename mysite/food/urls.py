from django.urls import path
from food import views

urlpatterns = [
    path('<int:pk>/', views.manage),
]
