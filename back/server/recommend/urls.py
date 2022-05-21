from django.urls import path, include
from . import views
from rest_framework import urls

urlpatterns = [
    path('select/<str:pk>', views.ingre_list),
    path('nutrition', views.nutrition),
    path('like', views.like),
    path('nutrition_result', views.nutrition_result),
    path('like_result', views.like_result),
]
