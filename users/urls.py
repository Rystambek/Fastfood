from .views import SignupView, ProfileView, UpdateProfileView, BuyingView, BuyFoodView
from django.urls import path


app_name = 'users'
urlpatterns = [
    path('signup', SignupView.as_view(), name='signup'),
    path('Profile/<str:username>', ProfileView.as_view(), name='Profile'),
    path('update', UpdateProfileView.as_view(), name='update'),
    path('buyafood/<int:food_id>', BuyingView.as_view(), name='buyafood'),
    path('buyed', BuyFoodView.as_view(), name='buyed'),
]
