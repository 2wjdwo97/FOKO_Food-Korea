from django.urls import path, include
from django.contrib import admin
from rest_framework import routers, serializers, viewsets

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('users/', include('user.urls')),
    path('foods/', include('food.urls')),
    path('reviews/', include('review.urls')),

    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('imageupload/', include('ocr.urls')),
]
