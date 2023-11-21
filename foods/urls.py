from django.urls import path
from .views import new_food


app_name = 'foods'
urlpatterns = [
    path("new", new_food, name='add'),
]
