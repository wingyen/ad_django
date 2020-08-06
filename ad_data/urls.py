from django.conf.urls import url
from django.urls import path
from ad_data.views import use_cases
from rest_framework import routers
router = routers.SimpleRouter()


urlpatterns = [
    url(r'^use_cases/$', use_cases),
]
