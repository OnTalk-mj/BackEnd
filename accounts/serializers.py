from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken

class Profile(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'birth', 'phone', 'address', 'zipcode']
        read_only_fields = ['username', 'email']

class Signup(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'name', 'birth', 'phone', 'address', 'zipcode']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")
        validate_password(data['password'])
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user

class Login(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"email": "등록된 이메일이 없습니다."})

        if not user.check_password(password):
            raise serializers.ValidationError({"password": "비밀번호가 틀렸습니다."})

        if not user.is_active:
            raise serializers.ValidationError({"email": "비활성화된 계정입니다."})

        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }