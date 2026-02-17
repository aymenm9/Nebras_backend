from rest_framework.serializers import ModelSerializer
from .models import Device

class DeviceSerializer(ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'
        read_only_fields = ['id', 'created_at','updated_at','is_active']
    
    def create(self, validated_data):
        device, created = Device.objects.update_or_create(token=validated_data['token'],defaults={
            'platform': validated_data['platform'],
            'is_active': validated_data['is_active']
        })
        return device