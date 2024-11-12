from django.contrib.auth.hashers import make_password
from django.utils import timezone

from rest_framework import serializers

from accounts import models
from accounts.models import Language


class LawyerRegisterSerializer(serializers.Serializer):
    full_name = serializers.CharField()
    phone_number = serializers.CharField(max_length=15)
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        password = data['password']
        confirm_password = data['confirm_password']
        if password != confirm_password:
            raise serializers.ValidationError({'error_message': 'Ikki parol bir xil bolishi kerak'})
        return data

    def create(self, validated_data):
        user = models.User.objects.create_user(
            phone_number=validated_data['phone_number'],
            full_name=validated_data['full_name'],
            password=make_password(validated_data['password']),
            is_active=False,
            user_role=models.LAWYER,
            auth_type=models.PHONE_NUMBER,
        )
        code = user.generate_code(models.FOR_REGISTER)
        return {
            'message': 'Telefon raqamingizga sms kod yuborildi',
            'code': code
        }


class LawyerRegisterVerifySerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    code = serializers.CharField(min_length=1, max_length=5)

    def validate(self, data):
        phone_number = data['phone_number']

        try:
            user = models.User.objects.get(
                phone_number=phone_number, is_active=False,
                user_role=models.LAWYER, auth_type=models.PHONE_NUMBER
            )
            code = models.UserConformation.objects.get(code=data['code'], user=user)
        except models.User.DoesNotExist:
            raise serializers.ValidationError({'message': 'User topilmadi'})
        except models.UserConformation.DoesNotExist:
            raise serializers.ValidationError({'message': 'Kod xato'})

        if code.expires < timezone.now():
            raise serializers.ValidationError({'message': 'Kodni yaroqlilik muddati tugagan'})
        if code.is_used:
            raise serializers.ValidationError({'message': 'Kod ishlatilgan'})
        return data

    def save(self):
        user = models.User.objects.get(
            phone_number=self.validated_data['phone_number'], is_active=False,
            user_role=models.LAWYER, auth_type=models.PHONE_NUMBER
        )
        code = models.UserConformation.objects.get(code=self.validated_data['code'], user=user, is_used=True, expires__gt=timezone.now())
        user.is_active = True
        code.is_used = True
        user.save()
        code.save()
        return {
            'message': 'Muvaffaqiyali royxatdan otdingiz',
        }


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Language
        fields = ['id', 'name']


class LawyerRegisterProfileSerializer(serializers.ModelSerializer):
    languages = serializers.PrimaryKeyRelatedField(many=True, queryset=models.Language.objects.all())
    phone_number = serializers.CharField()
    class Meta:
        model = models.Lawyer
        fields = [
            'phone_number',
            'consultation',
            'consultation_price',
            'work_place',
            'profession',
            'license_status',
            'license_date',
            'bio',
            'telegram',
            'whatsapp',
            'inter_expires_has',
            'experience',
            'type',
            'card',
            'languages',
        ]


    def create(self, validated_data):
        user = models.User.objects.get(phone_number=validated_data['phone_number'])
        lawyer = models.Lawyer.objects.create(
            user=user,
            consultation=validated_data['consultation'],
            consultation_price=validated_data['consultation_price'],
            work_place=validated_data['work_place'],
            profession=validated_data['profession'],
            license_status=validated_data['license_status'],
            license_date=validated_data['license_date'],
            bio=validated_data['bio'],
            telegram=validated_data['telegram'],
            whatsapp=validated_data['whatsapp'],
            inter_expires_has=validated_data['inter_expires_has'],
            experience=validated_data['experience'],
            type=validated_data['type'],
            card=validated_data['card'],
        )
        languages = validated_data.pop('languages')
        lawyer.language.set(languages)
        lawyer.save()
        return {
            'message': 'muvaffaqiyatli royxatdan otdingiz'
        }


class CustomerRegisterSerializer(serializers.Serializer):
    full_name = serializers.CharField(min_length=1, max_length=100)
    phone_number = serializers.CharField(min_length=1, max_length=15)
    password = serializers.CharField(min_length=1, max_length=100)
    confirm_password = serializers.CharField(min_length=1, max_length=100)

    def validate(self, data):
        password = data['password']
        confirm_password = data['confirm_password']
        if password != confirm_password:
            raise serializers.ValidationError(
                {'message': 'ikki parol bir xil bolishi kerak'}
            )
        return data

    def create(self, validated_data):
        user = models.User.objects.create_user(
            phone_number=validated_data['phone_number'],
            full_name=validated_data['full_name'],
            password=make_password(validated_data['password']),
            is_active=False,
            user_role=models.CUSTOMER,
            auth_type=models.PHONE_NUMBER
        )
        code = user.generate_code(models.FOR_REGISTER)
        return {
            'message': 'Telefon raqamingizga sms kod yuborildi',
            'code': code
        }


class CustomerRegisterVerifySerializer(serializers.Serializer):
    phone_number = serializers.CharField(min_length=1, max_length=15)
    code = serializers.CharField(min_length=1, max_length=100)

    def validate(self, data):
        try:
            user = models.User.objects.get(phone_number=data['phone_number'], is_active=False, user_role=models.CUSTOMER, auth_type=models.PHONE_NUMBER)
            code = models.UserConformation.objects.get(code=data['code'], user=user)
        except models.User.DoesNotExist:
            raise serializers.ValidationError({'message': 'Foydalanuvchi topilmadi'})
        except models.UserConformation.DoesNotExist:
            raise serializers.ValidationError({'message': 'Kod topilmadi'})

        if code.expires < timezone.now():
            raise serializers.ValidationError({'message': 'Kod yaroqlilik muddati tugagan'})
        if code.is_used:
            raise serializers.ValidationError({'message': 'Kod ishlatilgan'})
        return data

    def save(self):
        user = models.User.objects.get(phone_number=self.validated_data['phone_number'])
        code = models.UserConformation.objects.get(code=self.validated_data['code'], user=user)
        user.is_active = True
        user.save()
        code.is_used = True
        code.save()
        return {
            'message': 'Muvaffaqiyali royxatdan otdingiz',
        }


class CustomerExtraPhoneSerializer(serializers.Serializer):
    phone_number = serializers.CharField(min_length=1, max_length=15)
    extra_phone_number = serializers.CharField(min_length=1, max_length=15)

    def validate(self, data):
        try:
            user = models.User.objects.get(phone_number=data['phone_number'], user_role=models.CUSTOMER, auth_type=models.PHONE_NUMBER)
        except models.User.DoesNotExist:
            raise serializers.ValidationError({'message': 'Foydalanuvchi topilmadi'})
        return data

    def save(self):
        user = models.User.objects.get(phone_number=self.validated_data['phone_number'], user_role=models.CUSTOMER, auth_type=models.PHONE_NUMBER)
        try:
            customer = models.Customer.objects.get(user=user)
        except models.Customer.DoesNotExist:
            raise serializers.ValidationError({'message': 'Foydalanuvchi topilmadi'})
        customer.extra_phone_number = self.validated_data['extra_phone_number']
        return customer


class ForgotPasswordSerializer(serializers.Serializer):
    phone_number = serializers.CharField(min_length=1, max_length=15)

    def validate(self, data):
        phone_number = data['phone_number']
        try:
            user = models.User.objects.get(phone_number=phone_number, auth_type=models.PHONE_NUMBER)
        except models.User.DoesNotExist:
            raise serializers.ValidationError({'message': 'Foydalanuvchi topilmadi'})
        return data

    def save(self):
        user = models.User.objects.get(phone_number=self.validated_data['phone_number'], auth_type=models.PHONE_NUMBER)
        code = user.generate_code(models.FOR_FORGOT_PASS)
        return {
            'message': 'Telefon raqamingizga sms kod yuborildi',
            'code': code
        }


class ForgotPasswordVerifySerializer(serializers.Serializer):
    phone_number = serializers.CharField(min_length=1, max_length=15)
    code = serializers.CharField(min_length=1, max_length=100)

    def validate(self, data):
        try:
            user = models.User.objects.get(phone_number=data['phone_number'], user_role=models.CUSTOMER, auth_type=models.PHONE_NUMBER)
            code = models.UserConformation.objects.get(code=data['code'], user=user, code_type=models.FOR_FORGOT_PASS)
        except models.UserConformation.DoesNotExist:
            raise serializers.ValidationError({'message': 'Kod topilmadi'})
        except models.User.DoesNotExist:
            raise serializers.ValidationError({'message': 'Foydalanuvchi topilmadi'})
        if code.expires < timezone.now():
            raise serializers.ValidationError({'message': 'Kod yaroqlilik muddati tugagan'})
        if code.is_used:
            raise serializers.ValidationError({'message': 'Kod ishlatilgan'})

        return data

    def save(self):
        user = models.User.objects.get(phone_number=self.validated_data['phone_number'])
        code = models.UserConformation.objects.get(code=self.validated_data['code'], user=user)
        code.is_used = True
        code.save()
        return {
            'message': 'Kod tasdiqlandi'
        }


class ForgotPasswordSetSerializer(serializers.Serializer):
    phone_number = serializers.CharField(min_length=1, max_length=15)
    password = serializers.CharField(min_length=1, max_length=100)
    confirm_password = serializers.CharField(min_length=1, max_length=100)

    def validate(self, data):
        try:
            user = models.User.objects.get(phone_number=data['phone_number'], auth_type=models.PHONE_NUMBER)
        except models.User.DoesNotExist:
            raise serializers.ValidationError({'message': 'Foydalanuvchi topilmadi'})
        password = data['password']
        confirm_password = data['confirm_password']
        if password != confirm_password:
            raise serializers.ValidationError({'message': 'ikki parol birxil bolishi kerak'})
        return data

    def save(self):
        user = models.User.objects.get(phone_number=self.validated_data['phone_number'], auth_type=models.PHONE_NUMBER)
        user.password = make_password(self.validated_data['password'])
        user.save()
        return user


class ResetPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(min_length=1, max_length=100)
    new_password = serializers.CharField(min_length=1, max_length=100)
    confirm_new_password = serializers.CharField(min_length=1, max_length=100)

    def validate(self, data):
        new_password = data['new_password']
        confirm_new_password = data['confirm_new_password']
        if new_password != confirm_new_password:
            raise serializers.ValidationError({'message': 'ikki parol bolishi kerak'})
        return data

    def save(self):
        user = self.context['request'].user
        if user.password != self.validated_data['old_password']:
            raise serializers.ValidationError({'message': 'Eski parol notogri'})
        user.password = make_password(self.validated_data['new_password'])
        user.save()
        return user


class ResendRegisterCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(min_length=1, max_length=15)

    def validate(self, data):
        try:
            user = models.User.objects.get(phone_number=data['phone_number'], auth_type=models.PHONE_NUMBER)
            code = models.UserConformation.objects.filter(user=user).first()
        except models.User.DoesNotExist:
            raise serializers.ValidationError({'message': 'Foydalanuvchi topilmadi'})
        if user.is_active:
            raise serializers.ValidationError({'message': 'User active holatda'})
        if code.expires > timezone.now():
            raise serializers.ValidationError({'message': 'Kod yaroqli'})
        return data

    def save(self):
        user = models.User.objects.get(phone_number=self.validated_data['phone_number'], auth_type=models.PHONE_NUMBER)
        code = user.generate_code(models.FOR_REGISTER)
        return {
            'message': 'kod yuborildi',
            'code': code,
        }


class ResendForgotPasswordCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(min_length=1, max_length=15)

    def validate(self, data):
        try:
            user = models.User.objects.get(phone_number=data['phone_number'], auth_type=models.PHONE_NUMBER)
            code = models.UserConformation.objects.filter(user=user).first()
        except models.User.DoesNotExist:
            raise serializers.ValidationError({'message': 'Foydalanuvchi topilmadi'})
        if user.is_active:
            raise serializers.ValidationError({'message': 'User active holatda'})
        if code.expires > timezone.now():
            raise serializers.ValidationError({'message': 'Kod yaroqli'})
        return data

    def save(self):
        user = models.User.objects.get(phone_number=self.validated_data['phone_number'], auth_type=models.PHONE_NUMBER)
        code = user.generate_code(models.FOR_FORGOT_PASS)
        return {
            'message': 'kod yuborildi',
            'code': code,
        }


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Region
        fields = ['id', 'name']


class CitySerializer(serializers.ModelSerializer):
    region = RegionSerializer(many=True, source='regions')
    class Meta:
        model = models.City
        fields = ['id', 'name', 'region']


class CountrySerializer(serializers.ModelSerializer):
    city = CitySerializer(many=True, source='cities')

    class Meta:
        model = models.Country
        fields = ['id', 'name', 'city']


class LocationTextEnterSerializer(serializers.Serializer):
    region_id = serializers.IntegerField()
    city_id = serializers.IntegerField()
    country_id = serializers.IntegerField()

    def validate(self, data):
        region_id = data['region_id']
        city_id = data['city_id']
        country_id = data['country_id']
        try:
            country = models.Country.objects.get(id=country_id)
            city = models.City.objects.get(id=city_id)
            region = models.Region.objects.get(id=region_id)
        except models.Country.DoesNotExist:
            raise serializers.ValidationError({'message': 'Bunday davlat mavjud emas'})
        except models.City.DoesNotExist:
            raise serializers.ValidationError({'message': 'Bunday shahar mavjud emas'})
        except models.Region.DoesNotExist:
            raise serializers.ValidationError({'message': 'Bunday tuman mavjud emas'})
        if city.country != country:
            raise serializers.ValidationError({'message': 'Bunday shahar siz tanlagan davlatda mavjud emas'})
        if region.city != city:
            raise serializers.ValidationError({'message': 'Bunday tuman siz tanlagan shaharda mavjud emas'})
        return data

    def save(self):
        user = self.context['request'].user
        country = models.Country.objects.get(country_id=self.validated_data['country_id'])
        city = models.City.objects.get(id=self.validated_data['city_id'], country=country)
        region = models.Region.objects.get(id=self.validated_data['region_id'], city=city)
        location = f'{country.name}, {city.name}, {region.name}'
        user.location_text = location
        user.save()
        return {
            'location': location,
            'user_location': user.location_text,
        }


class GetLocationSerializer(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()

    def save(self):
        user = self.context['request'].user
        user.latitude = self.validated_data['latitude']
        user.longitude = self.validated_data['longitude']
        user.save()
        return {
            'latitude': user.latitude,
            'longitude': user.longitude,
        }


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Profession
        fields = ['id', 'name']


class LawyerProfileSerializer(serializers.ModelSerializer):
    phone_number = serializers.SerializerMethodField(method_name='get_phone_number')
    full_name = serializers.SerializerMethodField(method_name='get_full_name')
    language = serializers.SerializerMethodField(method_name='get_language')
    # profile_photo = serializers.SerializerMethodField(method_name='get_profile_photo')
    gender = serializers.SerializerMethodField(method_name='get_gender')
    location_text = serializers.SerializerMethodField(method_name='get_location_text')
    email = serializers.SerializerMethodField(method_name='get_email')

    class Meta:
        model = models.Lawyer
        fields = [
            'id', 'phone_number', 'full_name', 'gender', 'location_text', 'email',
            'work_place', 'profession', 'consultation', 'consultation_price',
            'license_date', 'license_status', 'bio', 'telegram', 'whatsapp', 'inter_expires_has', 'experience', 'type',
            'card', 'language'
        ]

    def get_phone_number(self, obj):
        return obj.user.phone_number

    def get_full_name(self, obj):
        return obj.user.full_name

    # def get_profile_photo(self, obj):
    #     return obj.user.profile_image

    def get_gender(self, obj):
        return obj.user.gender

    def get_location_text(self, obj):
        return obj.user.location_text

    def get_email(self, obj):
        return obj.user.email

    def get_language(self, obj):
        return LanguageSerializer(obj.language, many=True).data



class CustomerProfileSerializer(serializers.ModelSerializer):
    phone_number = serializers.SerializerMethodField(method_name='get_phone_number')
    full_name = serializers.SerializerMethodField(method_name='get_full_name')
    gender = serializers.SerializerMethodField(method_name='get_gender')
    location_text = serializers.SerializerMethodField(method_name='get_location_text')
    email = serializers.SerializerMethodField(method_name='get_email')

    class Meta:
        model = models.Customer
        fields = [
            'id', 'phone_number', 'full_name', 'gender', 'location_text', 'email',
            'extra_phone',
        ]

    def get_phone_number(self, obj):
        return obj.user.phone_number

    def get_full_name(self, obj):
        return obj.user.full_name

    def get_gender(self, obj):
        return obj.user.gender

    def get_location_text(self, obj):
        return obj.user.location_text

    def get_email(self, obj):
        return obj.user.email