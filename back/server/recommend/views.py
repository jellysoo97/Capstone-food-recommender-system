from django.http import HttpResponse, JsonResponse
from django.core import serializers
import json
from rest_framework.parsers import JSONParser

from selectIngre.views import BestCombiGlv
from .models import *

# Create your views here.

def IngreBalance():
    best_combi_result = BestCombiGlv()
    
