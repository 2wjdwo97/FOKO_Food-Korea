from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from address import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^address/', views.address_list),
    url(r'^imageUpload/', views.imageUpload),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
