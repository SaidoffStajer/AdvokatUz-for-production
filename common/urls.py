from django.urls import path
from . import views

urlpatterns = [
    path('constitution', views.ConstitutionGenericAPIView.as_view(), name = 'constitution'),
    path('video-list/', views.VideoListCreateAPIView.as_view(), name = 'video-list-create'),
    path('news-list/', views.NewsListAPIView.as_view(), name = 'news-list'),
    path('news-detail/<int:pk>/', views.NewsRetrieveAPIView.as_view(), name = 'news-detail'),
    path('statistics-list/',views.StatisticsGenericAPIView.as_view(), name = 'statics'),
    path('lawyer-banner-list/',views.LawyerBannerListAPIView.as_view(), name = 'lawyer-banner'),
    
    
]