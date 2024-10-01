from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from apps.authentication.v1.serializers.sigup_sigiin_serializer import (
    SetPhoneNumberSerializer, TokenSerializer, RegisterSerializer)
from drf_spectacular.utils import extend_schema, OpenApiRequest, OpenApiResponse
from rest_framework import status
from django.core.cache import cache
from random import randint
import uuid

User = get_user_model()

class SettingPhoneNumberApi(APIView):
    serializer_class = SetPhoneNumberSerializer

    @extend_schema(responses=serializer_class, request=serializer_class)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            if phone_number is None:
                error = 'Phone number is required'
                return Response(data={'error': error}, status=status.HTTP_400_BAD_REQUEST)
            otp_code = randint(1000, 9999)
            # TODO send sms function otp in interface
            print(otp_code)
            token = str(uuid.uuid4())
            cache.set(f"{token}_phone_number", phone_number, timeout=300)
            cache.set(f"{token}_otp", otp_code, timeout=300)
            result = {'result': token}
            return Response(data=result)
        return Response(serializer.errors)


class VerifyOTPApi(APIView):
    serializer_class = TokenSerializer

    @extend_schema(responses=serializer_class, request=serializer_class)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data['token']
            otp = serializer.validated_data['otp']
            if not token or not otp:
                error = 'token or otp is not none'
                return Response(data={'error': error}, status=status.HTTP_400_BAD_REQUEST)
            stored_otp = cache.get(f"{token}_otp")
            print(stored_otp ,':', type(stored_otp))
            print(otp, ':', otp)
            if otp == str(stored_otp):
                result = {'token': token}
                return Response(data=result, status=status.HTTP_200_OK)
            else:
                error = 'otp code is not valid'
                return Response(data={'error': error}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data)




class RegisterUserApi(APIView):
    serializer_class = RegisterSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data['token']
            password = serializer.validated_data['password']
            if not token or not password:
                error = 'password and token is required'
                return Response(data={'error': error}, status=status.HTTP_400_BAD_REQUEST)
            phone_number = cache.get(f"{token}_phone_number")
            if phone_number is None:
                error = 'Invalid or expired token'
                return Response(data={'error': error}, status=status.HTTP_400_BAD_REQUEST)

            if User.objects.filter(uphone_number=phone_number).exists():
                error = 'phone number is exist'
                return Response(data={'error': error}, status=status.HTTP_400_BAD_REQUEST)
            User.objects.create_user(phone_number=phone_number, password=password)
            cache.delete(f"{token}_phone_number")
            result = {'message':'user created'}
            return Response(data=result, status=status.HTTP_200_OK)





