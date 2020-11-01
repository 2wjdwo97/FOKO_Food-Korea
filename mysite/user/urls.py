from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/', views.manage),
    path('signup/', views.signup),
    path('login/', views.login),
    path('taste/', views.set_user_taste),
    path('activate/<str:uidb64>/<str:token>/', views.activate),
    path('help/id/', views.find_id),
    path('help/pw/', views.find_pw),
    # path('logout/', views.logout, name='logout'),
]
