from .models import Food
from django import forms

class NewFoodForm(forms.ModelForm):
    # images = forms.ImageField(widget=forms.MultipleHiddenInput(attrs={'multiple': True}))
    image = forms.ImageField(required=False, label="Food image",
                             help_text="Please upload food image")
    class Meta:
        model = Food
        fields = ('title', 'description', 'price', 'category', 'phone_number', 'image')

    def save(self, request, commit=True):
        food = self.instance
        food.author = request.user
        super().save(commit)
        return food
    
class FoodForm(forms.ModelForm):
    # images = forms.ImageField(widget=forms.MultipleHiddenInput(attrs={'multiple': True}))
    image = forms.ImageField(required=False, label="Food image",
                             help_text="Please upload food image")
    
    class Meta:
        model = Food
        fields = ('title', 'description', 'price', 'category', 'phone_number', 'image')