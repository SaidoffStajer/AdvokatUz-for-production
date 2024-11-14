from rest_framework import serializers
from common.models import Constitution,News,Video
from hitcount.models import HitCount
from django.contrib.contenttypes.models import ContentType
from accounts.models import Lawyer

class ConstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Constitution
        fields = ['id', 'file','link']

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'user', 'video_file','youtube_link']


class NewsSerializer(serializers.ModelSerializer):
    hit_count = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = ['id', 'title','description','image','hit_count',]

    def get_hit_count(self, obj):
        # Retrieve the hit count for this Todo object
        hit_count = HitCount.objects.get_for_object(obj)
        return hit_count.hits

class StatisticsSerializer(serializers.Serializer):
    total_users = serializers.IntegerField()
    total_customers = serializers.IntegerField()
    total_lawyers = serializers.IntegerField()
    today_registered_users = serializers.IntegerField()
    
class LawyerBannersSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='user.full_name')
    profile_image = serializers.ImageField(source='user.profile_image')
    class Meta:
        model = Lawyer
        fields = ['id', 'full_name', 'profile_image', 'license_status']