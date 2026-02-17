from . import views
from django.urls import path

urlpatterns = [
    path('devices/', views.DeviceView.as_view(), name='create-device'),
    path('devices/<int:pk>/', views.DeviceDestroyView.as_view(), name='device-detail'),
    path('devices/deactivate/', views.DeviceDeactivateView.as_view(), name='deactivate-device'),
]
