from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSignupSerializer, UserLoginSerializer
from rest_framework.permissions import IsAuthenticated

class SignupView(APIView):
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "회원가입이 완료되었습니다!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmailCheckView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"error": "email is required."}, status=status.HTTP_400_BAD_REQUEST)

        from django.contrib.auth import get_user_model
        User = get_user_model()

        exists = User.objects.filter(email=email).exists()
        return Response({"exists": exists}, status=status.HTTP_200_OK)

class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        user_data = {
            "username": user.username,
            "email": user.email,
            "phone": getattr(user, 'phone', None),
        }
        return Response(user_data, status=status.HTTP_200_OK)

class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = request.user

        name = request.data.get('name')
        birthdate = request.data.get('birthdate')
        phone = request.data.get('phone')
        address = request.data.get('address')
        zipcode = request.data.get('zipcode')

        if name:
            user.name = name
        if birthdate:
            user.birthdate = birthdate
        if phone:
            user.phone = phone
        if address:
            user.address = address
        if zipcode:
            user.zipcode = zipcode

        user.save()

        return Response({"message": "회원 정보가 수정되었습니다!"}, status=status.HTTP_200_OK)