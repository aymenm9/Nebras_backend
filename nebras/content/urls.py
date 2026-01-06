from django.urls import path
from .views import (
    UploadYoutubeVideo, UploadYoutubeVideoDetail,
    R2FileUpload, R2FileUploadCreate, R2FileUploadDetail
)

urlpatterns = [
    path('youtube/', UploadYoutubeVideo.as_view(), name='youtube-list-create'),
    path('youtube/<int:pk>/', UploadYoutubeVideoDetail.as_view(), name='youtube-detail'),
    path('files/', R2FileUpload.as_view(), name='file-list'),
    path('files/upload/', R2FileUploadCreate.as_view(), name='file-upload'),
    path('files/<int:pk>/', R2FileUploadDetail.as_view(), name='file-detail'),
]
