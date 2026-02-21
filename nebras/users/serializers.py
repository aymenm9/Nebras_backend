from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile, Ban
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['profile_image']



class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    profile_image = serializers.ImageField(required=False, write_only=True)
    is_super_admin = serializers.BooleanField(source='is_superuser', read_only=True)
    is_moderator = serializers.BooleanField(source='is_staff', read_only=True)
    

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile', 'is_super_admin', 'is_moderator','first_name','last_name','profile_image']
        extra_kwargs = {'password': {'write_only': True}, 'is_staff': {'read_only': True},
        'is_superuser': {'read_only': True}}

    def create(self, validated_data):
        profile_image = validated_data.pop('profile_image', None)
        user = User.objects.create(**validated_data)
        profile = Profile.objects.create(user=user, profile_image=profile_image)
        user.set_password(validated_data['password'])
        user.save()
        return user
    def update(self, instance, validated_data):
        profile_image = validated_data.pop('profile_image', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if profile_image is not None:
            if not hasattr(instance, 'profile'):
                Profile.objects.create(user=instance, profile_image=profile_image)
            else:
                instance.profile.profile_image = profile_image
                instance.profile.save()
        return instance
       



class ModeratorSerializer(serializers.ModelSerializer):
    #profile = ProfileSerializer()
    profile_image = serializers.ImageField(required=False)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password','first_name','last_name','profile_image','is_active']
        extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data):
        profile_image = validated_data.pop('profile_image', None)
        user = User.objects.create(**validated_data)
        profile = Profile.objects.create(user=user, profile_image=profile_image)
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def update(self, instance, validated_data):
        profile_image = validated_data.pop('profile_image', None)
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if profile_image is not None:
            if not hasattr(instance, 'profile'):
                Profile.objects.create(user=instance, profile_image=profile_image)
            else:
                instance.profile.profile_image = profile_image
                instance.profile.save()
        return instance

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

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()