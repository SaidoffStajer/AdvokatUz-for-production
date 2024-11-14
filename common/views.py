from django.shortcuts import render
from rest_framework import generics
from .models import Constitution,News,Video
from .serializers import ConstitutionSerializer,NewsSerializer,VideoSerializer,StatisticsSerializer,LawyerBannersSerializer
from rest_framework.response import Response
from rest_framework import status
from hitcount.models import HitCount
from hitcount.views import HitCountMixin
from django.contrib.contenttypes.models import ContentType
from rest_framework.permissions import IsAuthenticated
from accounts.models import User,Lawyer

from datetime import date

# Create your views here.



class ConstitutionGenericAPIView(generics.GenericAPIView):
    queryset = Constitution.objects.all()
    serializer_class = ConstitutionSerializer


class VideoListCreateAPIView(generics.ListCreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

class NewsListAPIView(generics.ListAPIView):

    queryset = News.objects.order_by('-created_at')[:10]
    serializer_class = NewsSerializer




class NewsRetrieveAPIView(generics.RetrieveAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    # permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

      
        self.increase_hit_count(instance)

        return super().retrieve(request, *args, **kwargs)

    def increase_hit_count(self, instance):
        hit_count, created = HitCount.objects.get_or_create(object_pk=instance.pk, content_type=self.get_content_type())
        hit_count.hits += 1
        hit_count.save()

    def get_content_type(self):
        from django.contrib.contenttypes.models import ContentType
        return ContentType.objects.get_for_model(News)

class StatisticsGenericAPIView(generics.GenericAPIView):
    serializer_class = StatisticsSerializer

    def get(self, request, *args, **kwargs):
        # Statistik ma'lumotlarni hisoblaymiz
        total_users = User.objects.count()
        total_customers = User.objects.filter(user_role='mijoz').count()
        total_lawyers = User.objects.filter(user_role='advokat').count()
        today_registered_users = User.objects.filter(created_at__date=date.today()).count()

        # Ma'lumotlarni serializer orqali formatlash
        data = {
            "total_users": total_users,
            "total_customers": total_customers,
            "total_lawyers": total_lawyers,
            "today_registered_users": today_registered_users,
        }
        serializer = self.get_serializer(data)
        return Response(serializer.data)
        
class LawyerBannerListAPIView(generics.ListAPIView):
    queryset = Lawyer.objects.all()
    serializer_class = LawyerBannersSerializer
    
    
