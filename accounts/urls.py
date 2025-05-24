from django.urls import path
from .views import SignupView, LoginView, EmailCheckView, UserInfoView, UserUpdateView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('id-check/', EmailCheckView.as_view(), name='id-check'),
    path('mypage/', UserInfoView.as_view(), name='userinfo'),
    path('mypage/update/', UserUpdateView.as_view(), name='userinfo-update'),
]
