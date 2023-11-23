from django.shortcuts import render, redirect
from .forms import SignupForm, UpdateProfileForm
from django.views import View
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import CustomUser, Saved
from django.contrib.auth.mixins import LoginRequiredMixin
from foods.models import Food


class SignupView(SuccessMessageMixin, View):
    def get(self, request):
        return render(request, 'registration/signup.html', {'form': SignupForm()})
    
    def post(self, request):
        form = SignupForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account is successfully created.')
            return redirect('login')
        return render(request, 'registration/signup.html', {'form': form})

    
class ProfileView(View):
    def get(self, request, username):
        user = get_object_or_404(CustomUser, username=username)
        return render(request, 'profile.html', {'customuser':user})
    
class UpdateProfileView(LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, request):
        form = UpdateProfileForm(instance=request.user)
        return render(request, 'profile_update.html', {'form':form})
    
    def post(self, request):
        form = UpdateProfileForm(instance=request.user, data=request.POST, files=request.FILES )
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account is successfully updated.')
            return redirect('users:profile', request.user)
        return render(request, 'registration/signup.html', {'form': form})
    
class BuyingView(LoginRequiredMixin, View):
    login_url = "login"
    def get(self, request, food_id):
        food = get_object_or_404(Food, id=food_id)
        buy_food = Saved.objects.filter(author=request.user, food=food)
        if buy_food:
            buy_food.delete()
            messages.info(request, 'Cancelled')
        else:
            Saved.objects.create(author=request.user, food=food)
            messages.info(request, 'Buy a food.')
        return redirect(request.META.get("HTTP_REFERER"))
    

class BuyFoodView(LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, request):
        saveds = Saved.objects.filter(author=request.user)
        food = Food.objects.filter()
        return render(request, 'buy_food.html', {'saveds':saveds})