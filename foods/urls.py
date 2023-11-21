from django.urls import path
from .views import new_food, food_detail, food_update, food_delete


app_name = 'foods'
urlpatterns = [
    path("new", new_food, name='new'),
    path('<int:food_id>/detail', food_detail, name='detail'),
    path('<int:food_id>/update', food_update, name='update'),
    path('<int:food_id>/delete', food_delete, name='delete'),
]
