from .models import Ingre
from rest_framework import serializers


class IngreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingre
        fields = "__all__"