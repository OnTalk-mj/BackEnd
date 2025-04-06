from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import Signup, Login, Profile
from .models import User

@api_view(['POST'])
def signup(request):
    serializer = Signup(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "회원가입 성공!"}, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def profile(request):
    user = request.user
    if user.is_authenticated:
        return Response({
            "username": user.username,
            "email": user.email,
            "name": user.name,
            "birth": user.birth,
            "phone": user.phone,
            "address": user.address,
            "zipcode": user.zipcode
        })
    return Response({"error": "인증되지 않음"}, status=401)

class LoginView(TokenObtainPairView):
    serializer_class = Login

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    serializer = Profile(request.user)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user_profile(request):
    serializer = Profile(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)