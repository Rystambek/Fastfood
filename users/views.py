from django.shortcuts import render, redirect
from .forms import SignupForm
from django.views import View
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import CustomUser

class SignupView(View):
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