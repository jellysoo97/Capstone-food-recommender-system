from django.urls import path
from selectIngre.views import *

urlpatterns = [
    path('group', getIngreGroup),
    path('group/<int:id>', getIngreSub),
    path('bestcombi/<int:pk>', BestCombi),
]