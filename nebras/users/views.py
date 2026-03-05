from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from drf_spectacular.utils import extend_schema
from rest_framework import serializers as drf_serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.throttling import ScopedRateThrottle
from .serializers import LoginSerializer, UserSerializer, PasswordChangeSerializer, ModeratorSerializer
from .permissions import IsModerator
from .throttles import UserLoginRateThrottle

class LoginView(APIView):
    """
    Login with username or email.
    """
    throttle_classes = [UserLoginRateThrottle]
    @extend_schema(
        request=LoginSerializer,
        responses={200: UserSerializer}
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        username_or_email = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        user = User.objects.filter(
            Q(username=username_or_email) | Q(email=username_or_email)
        ).first()
        
        if user and user.check_password(password):
            if not user.is_active:
                return Response({'error': 'Account is disabled'}, status=status.HTTP_403_FORBIDDEN)
            
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            })
        
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class MeView(APIView):
    """
    Get current user profile.
    """
    permission_classes = [IsAuthenticated, IsModerator]

    @extend_schema(
        responses={200: UserSerializer}
    )
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class EditProfileView(generics.UpdateAPIView):
    """
    Edit current user profile.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsModerator]

    def get_object(self):
        return self.request.user
    
class PasswordChangeView(APIView):
    """
    Change current user password.
    """
    permission_classes = [IsAuthenticated, IsModerator]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'password_change'




    @extend_schema(
        request=PasswordChangeSerializer,
        responses={
            200: None,
        },
        description="Change the password of the current user. Requires old_password and new_password in the request body."
    )
    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']

        if not user.check_password(old_password):
            return Response({'error': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({'message': 'Password changed successfully'})

