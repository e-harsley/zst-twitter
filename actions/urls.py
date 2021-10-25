
from django.urls import path
from .views import *


urlpatterns = [
    path('tweet/', ActivitiesApi.as_view())
]