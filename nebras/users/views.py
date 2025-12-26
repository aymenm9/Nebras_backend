from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .serializers import LoginSerializer, UserSerializer, ModeratorSerializer
from .permissions import IsSuperAdmin

class LoginView(APIView):
    """
    Login with username or email.
    """
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
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class ModeratorListCreateView(generics.ListCreateAPIView):
    """
    List and create moderators (Super Admin only).
    """
    queryset = User.objects.all()
    serializer_class = ModeratorSerializer
    permission_classes = [IsSuperAdmin]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['is_staff', 'is_superuser','is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    

    def get_queryset(self):
        return super().get_queryset().filter(is_staff=True).filter(is_superuser=False)


class ModeratorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a moderator (Super Admin only).
    """
    queryset = User.objects.all()
    serializer_class = ModeratorSerializer
    permission_classes = [IsSuperAdmin]

    def get_queryset(self):
        return super().get_queryset().filter(is_staff=True).filter(is_superuser=False)