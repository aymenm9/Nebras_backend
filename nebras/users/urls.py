from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import LoginView, MeView, ModeratorListCreateView, ModeratorRetrieveUpdateDestroyView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', MeView.as_view(), name='me'),
    path('moderators/', ModeratorListCreateView.as_view(), name='moderator_list_create'),
    path('moderators/<int:pk>/', ModeratorRetrieveUpdateDestroyView.as_view(), name='moderator_detail'),
]
