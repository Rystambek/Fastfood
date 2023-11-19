from django.shortcuts import render
from django.views import View
from foods.models import Food
# Create your views here.

class IndexView(View):
    def get(self, request):
        foods = Food.objects.all()
        return render(request, "index.html", {'foods':foods})