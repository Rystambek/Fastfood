from django.shortcuts import render, redirect
from .forms import NewFoodForm, FoodForm
from .models import FoodImage, Food
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='login')
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

@login_required(login_url='login')
def food_update(request, food_id):
    food = get_object_or_404(Food, id= food_id)
    if request.user==food.author:
        if request.method=='GET':
            form = FoodForm(instance=food)
            return render(request, 'update_food.html', {'form':form, 'fd':food})
        elif request.method=='POST':
            form = FoodForm(instance=food, data=request.POST, files=request.FILES)
            if form.is_valid():
                form.save()
                if request.FILES.getlist('images'):
                    FoodImage.objects.filter(food=food).delete()
                    for i in request.FILES.getlist('images'):
                        FoodImage.objects.create(food=food, image=i)
                messages.success(request, 'Successfully updated')
                return redirect('main:index')
            return render(request, 'update_food.html', {'form': form, 'fd':food})
        else:
            messages.error(request, 'Access danied')
            return redirect('main:index')
        

def food_delete(request, food_id):
    food = get_object_or_404(Food, id=food_id)
    if request.user==food.author:
        if request.method=='POST':
            food.delete()
            messages.info(request, 'Successfully deleted!')
            return redirect('main:index')
        return render(request, 'delete_food.html', {'food':food})
    else:
        messages.error(request, 'Access danied')
        return redirect('main:index')