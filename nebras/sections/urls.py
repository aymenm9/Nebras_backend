from django.urls import path
from .views import (
    MainSectionListCreateView, MainSectionRetrieveUpdateDestroyView,
    SubSectionListCreateView, SubSectionRetrieveUpdateDestroyView,
    SecondarySubSectionListCreateView, SecondarySubSectionRetrieveUpdateDestroyView,
    PublicMainSectionListView, PublicSubSectionListView, PublicSecondarySubSectionListView,
    PublicMainSectionRetrieveView, PublicSubSectionRetrieveView, PublicSecondarySubSectionRetrieveView
)

urlpatterns = [
    # Private / Staff endpoints
    path('main/', MainSectionListCreateView.as_view(), name='main-section-list'),
    path('main/<int:pk>/', MainSectionRetrieveUpdateDestroyView.as_view(), name='main-section-detail'),
    path('sub/', SubSectionListCreateView.as_view(), name='sub-section-list'),
    path('sub/<int:pk>/', SubSectionRetrieveUpdateDestroyView.as_view(), name='sub-section-detail'),
    path('secondary/', SecondarySubSectionListCreateView.as_view(), name='secondary-sub-section-list'),
    path('secondary/<int:pk>/', SecondarySubSectionRetrieveUpdateDestroyView.as_view(), name='secondary-sub-section-detail'),

    # Public endpoints
    path('public/main/', PublicMainSectionListView.as_view(), name='public-main-section-list'),
    path('public/main/<int:pk>/', PublicMainSectionRetrieveView.as_view(), name='public-main-section-detail'),
    path('public/sub/', PublicSubSectionListView.as_view(), name='public-sub-section-list'),
    path('public/sub/<int:pk>/', PublicSubSectionRetrieveView.as_view(), name='public-sub-section-detail'),
    path('public/secondary/', PublicSecondarySubSectionListView.as_view(), name='public-secondary-sub-section-list'),
    path('public/secondary/<int:pk>/', PublicSecondarySubSectionRetrieveView.as_view(), name='public-secondary-sub-section-detail'),
]
