from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup),
    path('login/', views.login),
    path('taste/', views.set_user_taste),
    path('activate/<str:uidb64>/<str:token>/', views.activate),

    path('help/id/', views.find_id),
    path('help/pw/', views.find_pw),

    path('get/', views.get_user),
    path('modify/', views.modify_user),
    path('modify/pw/', views.change_pw),
    path('delete/', views.delete_user)
    # path('logout/', views.logout, name='logout'),
]
