from django.urls import path
from .views import (
    PublicMainSectionListView, PublicMainSectionRetrieveView,
    PublicSubSectionListView, PublicSubSectionRetrieveView,
    PublicSecondarySubSectionListView, PublicSecondarySubSectionRetrieveView,
    PublishYoutubeVideo, PublishYoutubeVideoDetail,
    PublishMetadata, PublishMetadataDetail,
    PublishR2File, PublishR2FileDetail
)

urlpatterns = [
    # Section endpoints
    path('sections/main/', PublicMainSectionListView.as_view(), name='public-main-section-list'),
    path('sections/main/<int:pk>/', PublicMainSectionRetrieveView.as_view(), name='public-main-section-detail'),
    path('sections/sub/', PublicSubSectionListView.as_view(), name='public-sub-section-list'),
    path('sections/sub/<int:pk>/', PublicSubSectionRetrieveView.as_view(), name='public-sub-section-detail'),
    path('sections/secondary/', PublicSecondarySubSectionListView.as_view(), name='public-secondary-sub-section-list'),
    path('sections/secondary/<int:pk>/', PublicSecondarySubSectionRetrieveView.as_view(), name='public-secondary-sub-section-detail'),

    # Content endpoints
    path('youtube/', PublishYoutubeVideo.as_view(), name='public-youtube-list'),
    path('youtube/<int:pk>/', PublishYoutubeVideoDetail.as_view(), name='public-youtube-detail'),
    path('metadata/', PublishMetadata.as_view(), name='public-metadata-list'),
    path('metadata/<int:pk>/', PublishMetadataDetail.as_view(), name='public-metadata-detail'),
    path('files/', PublishR2File.as_view(), name='public-r2file-list'),
    path('files/<int:pk>/', PublishR2FileDetail.as_view(), name='public-r2file-detail'),
]
