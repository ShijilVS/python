from django.urls import path
from knox import views as knox_views
from .views import RegisterAPI, LoginAPI, TimerView
from .views import TimerView, ElapsedTimeView
urlpatterns = [
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('api/timer/', TimerView.as_view(), name='timer'),
    path('timer/', TimerView.as_view(), name='timer'),
    path('elapsed-time/', ElapsedTimeView.as_view(), name='elapsed_time'),
]