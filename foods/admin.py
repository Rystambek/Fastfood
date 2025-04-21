from django.contrib import admin
from .models import Comment, Category, Food, FoodImage
from .models import Feedback

admin.site.register(Feedback)

# Register your models here.

class FoodImageInline(admin.TabularInline):
    model = FoodImage

class FoodAdmin(admin.ModelAdmin):
    list_display = ['title', 'id', 'date', 'category', "author"]
    inlines = [FoodImageInline]



admin.site.register(Comment)
admin.site.register(FoodImage)
admin.site.register(Food, FoodAdmin)
admin.site.register(Category)