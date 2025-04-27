from django.urls import path
from .views import SignupView, LoginView, EmailCheckView, UserInfoView, UserUpdateView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('email-check/', EmailCheckView.as_view(), name='email-check'),
    path('mypage/', UserInfoView.as_view(), name='userinfo'),
    path('mypage/update/', UserUpdateView.as_view(), name='userinfo-update'),
]
