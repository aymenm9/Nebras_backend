from django.urls import path
from . import views

urlpatterns = [
    # Moderator Management
    path('moderators/', views.AdminModeratorListCreateView.as_view(), name='admin-moderator-list-create'),
    path('moderators/<int:pk>/', views.AdminModeratorRetrieveUpdateDestroyView.as_view(), name='admin-moderator-detail'),

    # Ban Management
    path('bans/', views.AdminBanUserView.as_view(), name='admin-ban-list-create'),
    path('bans/<int:pk>/', views.AdminBanUserRetrieveUpdateDestroyView.as_view(), name='admin-ban-detail'),

    # Section Management (List and RUD Only)
    path('sections/main/', views.AdminMainSectionListView.as_view(), name='admin-main-section-list'),
    path('sections/main/<int:pk>/', views.AdminMainSectionRetrieveUpdateDestroyView.as_view(), name='admin-main-section-detail'),
    
    path('sections/sub/', views.AdminSubSectionListView.as_view(), name='admin-sub-section-list'),
    path('sections/sub/<int:pk>/', views.AdminSubSectionRetrieveUpdateDestroyView.as_view(), name='admin-sub-section-detail'),
    
    path('sections/secondary/', views.AdminSecondarySubSectionListView.as_view(), name='admin-secondary-sub-section-list'),
    path('sections/secondary/<int:pk>/', views.AdminSecondarySubSectionRetrieveUpdateDestroyView.as_view(), name='admin-secondary-sub-section-detail'),

    # Content Management (List and RUD Only)
    path('content/youtube/', views.AdminYoutubeVideoListView.as_view(), name='admin-youtube-list'),
    path('content/youtube/<int:pk>/', views.AdminYoutubeVideoRetrieveUpdateDestroyView.as_view(), name='admin-youtube-detail'),
    
    path('content/files/', views.AdminR2FileListView.as_view(), name='admin-file-list'),
    path('content/files/<int:pk>/', views.AdminR2FileRetrieveUpdateDestroyView.as_view(), name='admin-file-detail'),

    # Chat Management
    path('chat/messages/', views.AdminChatMessageListView.as_view(), name='admin-chat-message-list'),
    path('chat/messages/<int:pk>/', views.AdminChatMessageRetrieveUpdateDestroyView.as_view(), name='admin-chat-message-detail'),
    path('chat/files/', views.AdminMessageFileListView.as_view(), name='admin-chat-file-list'),
    path('chat/files/<int:pk>/', views.AdminMessageFileRetrieveUpdateDestroyView.as_view(), name='admin-chat-file-detail'),
]
