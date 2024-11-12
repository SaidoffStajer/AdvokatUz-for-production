
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from accounts import serializers, models


class LawyerRegisterApiView(generics.GenericAPIView):
    serializer_class = serializers.LawyerRegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LawyerRegisterVerifyApiView(generics.GenericAPIView):
    serializer_class = serializers.LawyerRegisterVerifySerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Muvaffaqiyatli royxatdan otdingiz'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LawyerRegisterProfileApiView(generics.GenericAPIView):
    serializer_class = serializers.LawyerRegisterProfileSerializer
    parser_classes = []
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.save(), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerRegisterApiView(generics.GenericAPIView):
    serializer_class = serializers.CustomerRegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.save(), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerRegisterVerifyApiView(generics.GenericAPIView):
    serializer_class = serializers.CustomerRegisterVerifySerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerExtraPhoneApiView(generics.GenericAPIView):
    serializer_class = serializers.CustomerExtraPhoneSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Telefon raqam saqlandi'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordApiView(generics.GenericAPIView):
    serializer_class = serializers.ForgotPasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordVerifyApiView(generics.GenericAPIView):
    serializer_class = serializers.ForgotPasswordVerifySerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = serializer.save()
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordSetApiView(generics.GenericAPIView):
    serializer_class = serializers.ForgotPasswordSetSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Parol muvaffaqiyatli ozgartirildi'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordApiView(generics.GenericAPIView):
    serializer_class = serializers.ResetPasswordSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response({"message": 'Parol muvaffaqiyatli ozgartirildi'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResendRegisterCodeApiView(generics.GenericAPIView):
    serializer_class = serializers.ResendRegisterCodeSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResendForgotPasswordCodeApiView(generics.GenericAPIView):
    serializer_class = serializers.ResendForgotPasswordCodeSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutApiView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = serializers.LogoutSerializer

    def post(self, request):
        try:
            refresh = request.data['refresh_token']
            token = RefreshToken(refresh)
            token.blacklist()
            return Response({'message': 'Akkaountdan muvaffaqiyatli chiqish qildingiz'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RegionListApiView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated,  ]
    serializer_class = serializers.CountrySerializer

    def get(self, request):
        countries = models.Country.objects.all()
        serializer = serializers.CountrySerializer(countries, many=True)
        return Response(serializer.data)


class LocationTextEnterApiView(generics.GenericAPIView):
    serializer_class = serializers.LocationTextEnterSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetLocationApiView(generics.GenericAPIView):
    serializer_class = serializers.GetLocationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.save(), status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LanguageListApiView(generics.ListAPIView):
    serializer_class = serializers.LanguageSerializer
    queryset = models.Language.objects.all()

class ProfessionListApiView(generics.ListAPIView):
    serializer_class = serializers.ProfessionSerializer
    queryset = models.Profession.objects.all()



class LawyerProfileDetailApiView(generics.GenericAPIView):
    serializer_class = serializers.LawyerProfileSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request, lawyer_id):
        try:
            lawyer = models.Lawyer.objects.get(id=lawyer_id)
        except models.Lawyer.DoesNotExist:
            return Response({'message': 'Lawyer is not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(lawyer)
        return Response(serializer.data)


class CustomerProfileDetailApiView(generics.GenericAPIView):
    serializer_class = serializers.CustomerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, customer_id):
        try:
            customer = models.Customer.objects.get(id=customer_id)
        except models.Customer.DoesNotExist:
            return Response({'message': 'Customer is not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(customer)
        return Response(serializer.data)
