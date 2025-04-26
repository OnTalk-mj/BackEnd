from django.urls import path
from .views import CounselingCenterListView

urlpatterns = [
    path('', CounselingCenterListView.as_view(), name='center-list'),
]
