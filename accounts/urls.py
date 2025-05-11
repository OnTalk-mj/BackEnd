from django.urls import path
from .views import SignupView, LoginView, IDCheckView, UserInfoView, UserUpdateView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('id-check/', IDCheckView.as_view(), name='id-check'),\
    path('mypage/', UserInfoView.as_view(), name='userinfo'),
    path('mypage/update/', UserUpdateView.as_view(), name='userinfo-update'),
]
