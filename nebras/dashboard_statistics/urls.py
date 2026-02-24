from django.urls import path
from . import views

urlpatterns = [
    path('moderator/totals/', views.ModeratorTotalsView.as_view(), name='moderator-totals'),
    path('moderator/content-distribution/', views.ModeratorContentDistributionView.as_view(), name='moderator-content-distribution'),
    path('moderator/content-added-chart/', views.ModeratorContentAddedChartView.as_view(), name='moderator-content-added-chart'),
]