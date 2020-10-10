from django.urls import path
from users import views

urlpatterns = [
    path('<int:pk>', views.manage_user),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('taste_setting/', views.set_user_taste),
    # path('logout/', views.logout, name='logout'),
]
