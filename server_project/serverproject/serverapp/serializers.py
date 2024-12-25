from rest_framework import serializers
from .models import ClientInfo

class ClientInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientInfo
        fields = ['name', 'ip', 'port']

class FileUploadSerialiser(serializers.Serializer):
    class Meta:
        model = ClientInfo
        fields = ['id', 'model_file']
    def update(self, instance, validate_data):
        instance.model_file = validate_data('model_file', instance.model_file)
        instance.save()
        return instance