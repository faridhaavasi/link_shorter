from rest_framework import serializers
from rest_framework.serializers import ValidationError
def check_start_whit_zero(value: str) -> str:
    if value[0] == '0' and value[1] == '9':
        return value
    raise ValidationError('format is not valid start phone_number must whit 09')
class SetPhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11, validators=[check_start_whit_zero,])


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    otp = serializers.CharField(required=True)


class RegisterSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
