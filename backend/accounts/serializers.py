from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User

class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password2', 'name', 'birth', 'phone', 'address', 'zipcode')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "비밀번호가 일치하지 않습니다!"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        email = validated_data.get('email')
        validated_data['username'] = email

        user = User.objects.create_user(**validated_data)
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(
                request=self.context.get('request'),  # 🔥 context의 request 넘기기
                email=email,
                password=password
            )
            if not user:
                raise serializers.ValidationError("잘못된 로그인 정보입니다.")
        else:
            raise serializers.ValidationError("이메일과 비밀번호를 모두 입력해주세요.")

        data['user'] = user
        return data
