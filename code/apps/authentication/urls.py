from django.urls import path
from apps.authentication.v1.views.sign_up import SettingPhoneNumberApi, VerifyOTPApi, RegisterUserApi

app_name = 'authentication'

urlpatterns = [
    path('settphonenumber', SettingPhoneNumberApi.as_view(), name='settphoneumber'),
    path('veryfiotp', VerifyOTPApi.as_view(), name='veryfi'),
    path('register', RegisterUserApi.as_view(), name='register_user')
]