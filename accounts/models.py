import random
import datetime

from django.utils import timezone
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from rest_framework_simplejwt.tokens import RefreshToken

from accounts.managers import CustomUserManager
from common.models import BaseModel

LAWYER, CUSTOMER = ('advokat', 'foydalanuvchi')
PHONE_NUMBER, GOOGLE, FACEBOOK, LINKEDIN = ('telefon raqam', 'google', 'facebook', 'linkedin')
MALE, FEMALE = ('erkak', 'ayol')
FOR_REGISTER, FOR_FORGOT_PASS = ('register uchun', 'forgot password uchun')
ACTIVE, DEACTIVE = ('faol', 'faolemas')
WORKER, FREELANCER = ('ishchi', 'freelancer')
FREE, STANDART,PRO,PREMIUM = ('free','standard','pro','premium')


class Language(BaseModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = _('til')
        verbose_name = _('tillar')


class User(AbstractUser, BaseModel):
    AUTH_TYPE = (
        (PHONE_NUMBER, PHONE_NUMBER,),
        (GOOGLE, GOOGLE),
        (FACEBOOK, FACEBOOK),
        (LINKEDIN, LINKEDIN),
    )
    USER_ROLE = (
        (LAWYER, LAWYER),
        (CUSTOMER, CUSTOMER),
    )
    GENDER = (
        (MALE, MALE),
        (FEMALE, FEMALE),
    )

    phone_number = models.CharField(
        max_length=15, unique=True, null=True, blank=True,
        validators=[RegexValidator(regex=r'^\+998\d{9}$', message="Telefon raqami notogri formatda")]
    )
    full_name = models.CharField(max_length=250)
    email = models.EmailField(unique=True, null=True, blank=True)
    auth_type = models.CharField(max_length=50, choices=AUTH_TYPE)
    user_role = models.CharField(max_length=50, choices=USER_ROLE)
    profile_image = models.ImageField(upload_to="media/accounts/user/profile-image/", null=True, blank=True)
    gender = models.CharField(max_length=50, choices=GENDER)
    location_text = models.CharField(max_length=250, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    username = None

    objects = CustomUserManager()
    REQUIRED_FIELDS = ['full_name']
    USERNAME_FIELD = 'phone_number'

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('userlar')

    def generate_code(self, code_type):
        code = ''.join([str(random.randint(0, 9)) for _ in range(5)])
        UserConformation.objects.create(
            code=code, user=self, code_type=code_type,
            expires=timezone.now() + datetime.timedelta(minutes=2)
        )
        return code

    def tokens(self):
        token = RefreshToken.for_user(self)
        return {
            'refresh_token': str(token),
            'access_token': str(token.access_token),
        }

class UserConformation(BaseModel):
    CODE_TYPE = (
        (FOR_REGISTER, FOR_REGISTER,),
        (FOR_FORGOT_PASS, FOR_FORGOT_PASS,)
    )
    code = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conformations')
    expires = models.DateTimeField(null=True, blank=True)
    is_used = models.BooleanField(default=False)
    code_type = models.CharField(max_length=50, choices=CODE_TYPE)

    def __str__(self):
        return f'{self.user.full_name} - {self.code}'

    class Meta:
        verbose_name = _('Tasdiqlash kodi')
        verbose_name_plural = _('Tasdiqlash kodlari')

class Lawyer(BaseModel):
    LICENSE_STATUS = (
        (ACTIVE, ACTIVE),
        (DEACTIVE, DEACTIVE)
    )
    LAWYER_TYPE = (
        (FREELANCER, FREELANCER),
        (WORKER, WORKER)
    )
    NAME = (
        (FREE, FREE),
        (STANDART, STANDART),
        (PRO, PRO),
        (PREMIUM, PREMIUM),
    )
    consultation = models.CharField(max_length=250, choices=NAME)
    consultation_price = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lawyers')
    work_place = models.CharField(max_length=50)
    profession = models.ForeignKey('Profession',on_delete=models.CASCADE, related_name='lawyers')
    license_date = models.DateField(null=True, blank=True)
    license_status = models.CharField(max_length=250, choices=LICENSE_STATUS)
    bio = models.TextField()
    telegram = models.CharField(max_length=250)
    whatsapp = models.CharField(max_length=250)
    inter_expires_has = models.BooleanField(default=False)
    experience = models.CharField(max_length=250)
    type = models.CharField(max_length=250, choices=LAWYER_TYPE)
    card = models.CharField(max_length=250)
    language = models.ManyToManyField(Language, related_name='lawyers')


    def __str__(self):
        return self.user.full_name

    class Meta:
        verbose_name = _("advokat")
        verbose_name_plural = _('advokatlar')


class LawyerRate(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lawyer_rate')
    rate = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()

    def __str__(self):
        return f'{self.user} - {self.rate}'

    class Meta:
        verbose_name = _('sharx')
        verbose_name_plural = _('sharxlar')


class Customer(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customers')
    extra_phone = models.CharField(
        max_length=23, null=True, blank=True,
        validators=[RegexValidator(regex=r'^\+998\d{9}$', message="Telefon raqami notogri formatda")]
    )

    def __str__(self):
        return self.user.full_name

    class Meta:
        verbose_name = _('foydalanuchi')
        verbose_name_plural = _('foydalanuchilar')


class Profession(BaseModel):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("mutaxasisligi")
        verbose_name_plural = _("mutaxasisliklari")


class Country(BaseModel):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('davlat')
        verbose_name_plural = _('davlatlar')


class City(BaseModel):
    name = models.CharField(max_length=250)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='cities')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('shahar')
        verbose_name_plural = _('shaharlar')


class Region(BaseModel):
    name = models.CharField(max_length=250)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='regions')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('tuman')
        verbose_name_plural = _('tumanlar')
