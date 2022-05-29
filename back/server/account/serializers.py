from .models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['user_id', 'password', 'vege_type',]
                # fields = ['user_id', 'password', 'sex',
                #   'age', 'vege_type', 'alle_type']

