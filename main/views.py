from django.shortcuts import render
from django.views import View
from foods.models import Food, Category
from django.shortcuts import get_object_or_404
from django.core.cache import cache

# Create your views here.

def for_all_pages(request):
    categories = cache.get('all_categories')
    if categories is None:
        categories = Category.objects.all()
        cache.set('all_categories', categories, 3600)  # Cache for 1 hour
    return {"categories": categories}

class IndexView(View):
    def get(self, request):
        foods = Food.objects.all()
        return render(request, "index.html", {'foods':foods})
    
class CategoryView(View):
    def get(self, request, category_name):
        category = get_object_or_404(Category, name=category_name)
        foods = Food.objects.filter(category=category)
        return render(request, "category.html", {'foods':foods, "category":category})