from django.urls import path, include
from . import views
from rest_framework import urls

urlpatterns = [
    path('select/<str:pk>', views.ingre_list),
    path('recommend', views.ingre_combi)
]
