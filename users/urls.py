from .views import SignupView, ProfileView, UpdateProfileView
from django.urls import path


app_name = 'users'
urlpatterns = [
    path('signup', SignupView.as_view(), name='signup'),
    path('profile/<str:username>', ProfileView.as_view(), name='profile'),
    path('update', UpdateProfileView.as_view(), name='update'),
]
