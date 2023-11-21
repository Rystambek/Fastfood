from .models import Food
from django import forms

class NewFoodForm(forms.ModelForm):
    # images = forms.ImageField(widget=forms.MultipleHiddenInput(attrs={'multiple': True}))
    class Meta:
        model = Food
        fields = ('title', 'description', 'price', 'category', 'phone_number')

    def save(self, request, commit=True):
        food = self.instance
        food.author = request.user
        super().save(commit)
        return food
    
class FoodForm(forms.ModelForm):
    # images = forms.ImageField(widget=forms.MultipleHiddenInput(attrs={'multiple': True}))
    class Meta:
        model = Food
        fields = ('title', 'description', 'price', 'category', 'phone_number')