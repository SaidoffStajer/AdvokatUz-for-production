import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from hitcount.models import HitCount
from django.contrib.contenttypes.fields import GenericRelation




class BaseModel(models.Model):
    #id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Constitution(BaseModel):
    file = models.FileField(null=True,blank=True,verbose_name=_('File'))
    link = models.CharField(max_length=255,null=True,blank=True,verbose_name=_('File link'))
    
    class Meta:
        verbose_name = _('Konstitutsiya')
        verbose_name_plural = _('Konstitutsiyalar')


    

class Video(BaseModel):
    user = models.ForeignKey("accounts.Lawyer", on_delete=models.CASCADE, null=True, blank=True, related_name='videos', related_query_name='video')
    video_file = models.FileField(null=True, blank=True,verbose_name=_('Video file'))
    youtube_link = models.CharField(max_length=255,null=True, blank=True, verbose_name=_('YouTube link'))

    class Meta:
        verbose_name = _('Video')
        verbose_name_plural = _('Videolar')

class News(BaseModel):
    title  = models.CharField(max_length=255,verbose_name=_('Title'))
    description = models.TextField(verbose_name=_('Description'))
    image = models.ImageField(upload_to = 'news_images/', verbose_name=_('News image'))
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic')


    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = _('Yangilik')
        verbose_name_plural = _('Yangiliklar')
