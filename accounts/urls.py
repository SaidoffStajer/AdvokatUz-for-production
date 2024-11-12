
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts import views


urlpatterns = [
    # lawyer register
    path('lawyer/register/', views.LawyerRegisterApiView.as_view(), name='lawyer-register'),
    path('lawyer/register/verify/', views.LawyerRegisterVerifyApiView.as_view(), name='lawyer-register-verify'),
    path('lawyer/register/profile/', views.LawyerRegisterProfileApiView.as_view(), name='lawyer-register-profile'),
    # customer register
    path('customer/register/', views.CustomerRegisterApiView.as_view(), name='customer-register'),
    path('customer/register/verify/', views.CustomerRegisterVerifyApiView.as_view(), name='customer-register-verify'),
    path('customer/register/extra-info/', views.CustomerExtraPhoneApiView.as_view(), name='customer-register-extra-info'),
    # forgot password
    path('forgot-password/', views.ForgotPasswordApiView.as_view(), name='forogt-password'),
    path('forgot-password/verify/', views.ForgotPasswordVerifyApiView.as_view(), name='forgot-passqord-verify'),
    path('forgot-password/set/', views.ForgotPasswordSetApiView.as_view(), name='forgot-password-set'),
    # reset password
    path('reset-password/', views.ResetPasswordApiView.as_view(), name='reset-password'),
    # resend code
    path('resend-code/for-register/', views.ResendRegisterCodeApiView.as_view(), name='resend-code-for-register'),
    path('resend-code/for-forgot-password/', views.ResendForgotPasswordCodeApiView.as_view(), name='resend-code-for-password'),
    # user login and logout
    path('user/login/', TokenObtainPairView.as_view(), name='login'),
    path('user/logout/', views.LogoutApiView.as_view(), name='logout'),
    path('user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # region choice and list
    path('region/list/', views.RegionListApiView.as_view(), name='region-list'),
    path('region/choose/', views.LocationTextEnterApiView.as_view(), name='region-choose'),
    # get location
    path('get-location/', views.GetLocationApiView.as_view(), name='get-location'),
    # lists
    path('language/list/', views.LanguageListApiView.as_view(), name='language-list'),
    path('profession/list/', views.ProfessionListApiView.as_view(), name='profession-list'),
    # lawyer profile
    path('lawyer/profile/<int:lawyer_id>/', views.LawyerProfileDetailApiView.as_view(), name='lawyer-profile'),
    # customer profile
    path('customer/profile/<int:customer_id>/', views.CustomerProfileDetailApiView.as_view(), name='customer-profile'),
]
