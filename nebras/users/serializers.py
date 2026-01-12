from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile, Ban

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['profile_image']

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    is_super_admin = serializers.BooleanField(source='is_superuser', read_only=True)
    is_moderator = serializers.BooleanField(source='is_staff', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile', 'is_super_admin', 'is_moderator','first_name','last_name']
        extra_kwargs = {'password': {'write_only': True}, 'is_staff': {'read_only': True},
        'is_superuser': {'read_only': True}}

class ModeratorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password','first_name','last_name']
        extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data):
        # Default staff status to True for moderators
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data, is_staff=True)
        user.set_password(password)
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class BanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ban
        fields = '__all__'
        extra_kwargs = {'banned_by': {'read_only': True}}
    def create(self, validated_data):
        request = self.context.get('request')
        ban = Ban.objects.create(banned_by=request.user, **validated_data)
        return ban