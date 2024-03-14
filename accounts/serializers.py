from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    repeat_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'repeat_password', 'email', 'role', 'phone_number', 'location')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['repeat_password']:
            raise serializers.ValidationError({"password": "Password fields do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('repeat_password')
        user = User.objects.create_user(**validated_data)
        return user
