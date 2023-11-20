from django.shortcuts import render
from django.views import View
from foods.models import Food, Category
from django.shortcuts import get_object_or_404
# Create your views here.

def for_all_pages(request):
    categories = Category.objects.all()
    return {"categories":categories}

class IndexView(View):
    def get(self, request):
        foods = Food.objects.all()
        return render(request, "index.html", {'foods':foods,})
    
class CategoryView(View):
    def get(self, request, category_name):
        category = get_object_or_404(Category, name= category_name)
        foods = Food.objects.filter(category=category)
        return render(request, "category.html", {'foods':foods, "category":category})