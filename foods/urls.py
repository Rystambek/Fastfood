from django.urls import path
from .views import new_food, food_detail


app_name = 'foods'
urlpatterns = [
    path("new", new_food, name='new'),
    path('<int:food_id>/detail', food_detail, name='detail'),
]
