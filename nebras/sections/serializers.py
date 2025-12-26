from rest_framework import serializers
from .models import MainSection, SubSection, SecondarySubSection

class MainSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainSection
        fields = ['id', 'name', 'order_index', 'created_at', 'created_by']
        read_only_fields = ['created_at']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

class SubSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubSection
        fields = ['id', 'main_section', 'name', 'order_index', 'created_at', 'created_by']
        read_only_fields = ['created_at']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

class SecondarySubSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecondarySubSection
        fields = ['id', 'sub_section', 'name', 'order_index', 'created_at', 'created_by']
        read_only_fields = ['created_at']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)
