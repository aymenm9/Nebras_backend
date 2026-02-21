from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import LoginView, MeView, EditProfileView, PasswordChangeView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', MeView.as_view(), name='me'),
    path('me/edit/', EditProfileView.as_view(), name='edit_profile'),
    path('me/password/change/', PasswordChangeView.as_view(), name='change_password'),
]
