from django.urls import path
from .views import (
    UploadYoutubeVideo, UploadYoutubeVideoDetail,
    R2FileUpload, R2FileUploadDetail,
    MultipartUploadDetail, GetUploadURL,
    PartCreate, PartDetail,
    CompleteMultipartUpload
)

urlpatterns = [
    path('youtube/', UploadYoutubeVideo.as_view(), name='youtube-list-create'),
    path('youtube/<int:pk>/', UploadYoutubeVideoDetail.as_view(), name='youtube-detail'),
    path('files/', R2FileUpload.as_view(), name='file-list-create'),
    path('files/<int:pk>/', R2FileUploadDetail.as_view(), name='file-detail'),
    path('files/<int:pk>/upload-url/', GetUploadURL.as_view(), name='file-upload-url'),
    path('files/<int:pk>/complete/', CompleteMultipartUpload.as_view(), name='file-complete-upload'),
    path('multipart/<int:pk>/', MultipartUploadDetail.as_view(), name='multipart-detail'),
    path('parts/', PartCreate.as_view(), name='part-create'),
    path('parts/<int:pk>/', PartDetail.as_view(), name='part-detail'),
]
