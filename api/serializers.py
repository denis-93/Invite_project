from rest_framework import serializers
from .models import User
import re


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'phone', 'invite_code', 'authorization_code', 'self_code')
        read_only_fields = ('id', 'self_code',)

    def validate_phone(self, value):
        pattern_phone = r'\+7\d{10}'
        if re.match(pattern_phone, value):
            return value
        else:
            raise serializers.ValidationError('Неверный формат телефона')

    def validate_authorization_code(self, value):
        if value.isdigit():
            return value
        else:
            raise serializers.ValidationError('В коде должны быть только цифры!')



