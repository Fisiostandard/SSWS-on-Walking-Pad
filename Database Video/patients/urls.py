from django.urls import path
from . import views, api_views

app_name = 'patients'

urlpatterns = [
    path('share/<str:token>/', views.share_access, name='share_access'),
    path('share/<str:token>/video/<int:video_id>/', views.share_video_stream, name='share_video'),
    # API
    path('api/treadmill-session/', api_views.receive_treadmill_session, name='api_treadmill_session'),
]
