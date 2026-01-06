from django.urls import path
from .views import (
    MainSectionListCreateView, MainSectionRetrieveUpdateDestroyView,
    SubSectionListCreateView, SubSectionRetrieveUpdateDestroyView,
    SecondarySubSectionListCreateView, SecondarySubSectionRetrieveUpdateDestroyView
)

urlpatterns = [
    # Private / Staff endpoints
    path('main/', MainSectionListCreateView.as_view(), name='main-section-list'),
    path('main/<int:pk>/', MainSectionRetrieveUpdateDestroyView.as_view(), name='main-section-detail'),
    path('sub/', SubSectionListCreateView.as_view(), name='sub-section-list'),
    path('sub/<int:pk>/', SubSectionRetrieveUpdateDestroyView.as_view(), name='sub-section-detail'),
    path('secondary/', SecondarySubSectionListCreateView.as_view(), name='secondary-sub-section-list'),
    path('secondary/<int:pk>/', SecondarySubSectionRetrieveUpdateDestroyView.as_view(), name='secondary-sub-section-detail'),
]
