from django.urls import path
from . import views

app_name = 'foods'

urlpatterns = [
    path('new/', views.new_food, name='new'),
    path('detail/<int:food_id>/', views.food_detail, name='detail'),
    path('update/<int:food_id>/', views.food_update, name='update'),
    path('delete/<int:food_id>/', views.food_delete, name='delete'),
    path('upload-images/', views.upload_images, name='upload_images'),
]
