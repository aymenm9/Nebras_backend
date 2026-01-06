from django.urls import path
from .views import UploadYoutubeVideo, UploadYoutubeVideoDetail

urlpatterns = [
    path('youtube/', UploadYoutubeVideo.as_view(), name='youtube-list-create'),
    path('youtube/<int:pk>/', UploadYoutubeVideoDetail.as_view(), name='youtube-detail'),
]
