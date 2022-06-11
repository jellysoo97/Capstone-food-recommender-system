from django.urls import path
from firstPreference.views import * 

urlpatterns = [
    # path('check', check_preference),
    path("first", getFirstPrefer),
    path("last", postPrefer),
]
