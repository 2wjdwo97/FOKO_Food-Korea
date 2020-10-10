from django.urls import path, include
from django.contrib import admin
from rest_framework import routers, serializers, viewsets
from foods import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('foods/', include('foods.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
