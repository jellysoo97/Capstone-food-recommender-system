from django.urls import path, include
from . import views
from rest_framework import urls

urlpatterns = [
    path('account', views.account_list),
    path('account/<int:pk>', views.account),
    path('login/', views.login),
    path('api-auth/', include('rest_framework.urls')),
]