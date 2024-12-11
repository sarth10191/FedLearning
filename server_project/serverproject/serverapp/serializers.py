from rest_framework import serializers
from .models import ClientInfo

class ClientInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientInfo
        fields = ['name', 'ip', 'port']
