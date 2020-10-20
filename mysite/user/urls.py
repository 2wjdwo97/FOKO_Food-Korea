from django.urls import path
from user import views

urlpatterns = [
    path('<int:pk>/', views.manage),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('taste/', views.set_user_taste),
    # path('logout/', views.logout, name='logout'),
]
