from django.shortcuts import render, redirect
from .forms import NewFoodForm
from .models import FoodImage, Food
from django.contrib import messages
from django.shortcuts import get_object_or_404

# Create your views here.

def new_food(request):
    if request.method == "GET":
        form = NewFoodForm
        return render(request, 'new_foods.html', {'form':form})
    elif request.method == "POST":
        form = NewFoodForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            food = form.save(request)
            for image in request.FILES.getlist("images"):
                FoodImage.objects.create(image=image, food=food)
            messages.success(request, "Successfully created!!!")
            return redirect('main:index')
        return render(request, 'new_foods.html', {'form':form})
    
def food_detail(request, food_id):
    food = get_object_or_404(Food, id= food_id)
    return render(request, 'details_food.html', {'food':food})
