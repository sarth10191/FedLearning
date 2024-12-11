from rest_framework import serializers

class RegisterSerializer(serializers.Serializer):
    name=serializers.CharField(max_length=100)
    ip = serializers.IPAddressField(protocol='both')
    port=serializers.IntegerField()
    