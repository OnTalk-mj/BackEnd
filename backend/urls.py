from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/consult/', include('centers.urls')),
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
