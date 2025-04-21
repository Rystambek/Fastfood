from django import forms
from .models import Food, FoodImage, Category
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['comment', 'rating']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Fikringizni yozing...', 'rows': 3}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5})
        }

class MultipleFileInput(forms.ClearableFileInput):
    """
    Custom widget that supports multiple file uploads.
    """
    def __init__(self, attrs=None):
        super().__init__(attrs)
        if attrs is None:
            attrs = {}
        attrs['multiple'] = True
        self.attrs = attrs

    def value_from_datadict(self, data, files, name):
        if hasattr(files, 'getlist'):
            return files.getlist(name)
        return files.get(name)

class FoodImageForm(forms.Form):
    """
    Form for handling multiple image uploads with validation.
    """
    images = forms.FileField(
        widget=MultipleFileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*',
            'id': 'id_images'
        }),
        required=False,
        help_text='Select multiple images (PNG, JPG, JPEG)',
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])
        ]
    )

    def clean_images(self):
        """
        Custom validation for the images field.
        """
        images = self.cleaned_data.get('images')
        if not images:
            return []
            
        # Convert single file to list for consistent handling
        if not isinstance(images, list):
            images = [images]
            
        # Validate each file
        for image in images:
            if image.size > 5 * 1024 * 1024:  # 5MB limit
                raise ValidationError('Each image must be less than 5MB')
            if not image.content_type.startswith('image/'):
                raise ValidationError('Only image files are allowed')
                
        return images

    def save(self, food):
        """
        Save the uploaded images to the database.
        """
        images = self.cleaned_data.get('images', [])
        for image in images:
            FoodImage.objects.create(food=food, image=image)

class NewFoodForm(forms.ModelForm):
    """
    Form for creating a new Food object with enhanced image handling.
    """
    class Meta:
        model = Food
        fields = ['title', 'description', 'price', 'phone_number', 'category', 'main_image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter food title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter food description',
                'rows': 4
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter price',
                'min': 0,
                'step': 0.01
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'main_image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }

    def clean_main_image(self):
        """
        Validate the main image.
        """
        image = self.cleaned_data.get('main_image')
        if image:
            if image.size > 5 * 1024 * 1024:  # 5MB limit
                raise ValidationError('Image must be less than 5MB')
            if not image.content_type.startswith('image/'):
                raise ValidationError('Only image files are allowed')
        return image

    def clean_price(self):
        """
        Validate the price field.
        """
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise ValidationError('Price must be greater than 0')
        return price

    def save(self, request, commit=True):
        """
        Save the Food object and set the author.
        """
        food = super().save(commit=False)
        food.author = request.user
        
        if commit:
            food.save()
            
            # Handle main image
            if 'main_image' in self.cleaned_data and self.cleaned_data['main_image']:
                food.main_image = self.cleaned_data['main_image']
                food.save()
                
        return food

class FoodForm(forms.ModelForm):
    """
    Form for updating existing Food objects.
    """
    class Meta:
        model = Food
        fields = ['title', 'description', 'price', 'phone_number', 'category', 'main_image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter food title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter food description',
                'rows': 4
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter price',
                'min': 0,
                'step': 0.01
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'main_image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }

    def clean_main_image(self):
        """
        Validate the main image.
        """
        image = self.cleaned_data.get('main_image')
        if image:
            if image.size > 5 * 1024 * 1024:  # 5MB limit
                raise ValidationError('Image must be less than 5MB')
            if not image.content_type.startswith('image/'):
                raise ValidationError('Only image files are allowed')
        return image

    def clean_price(self):
        """
        Validate the price field.
        """
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise ValidationError('Price must be greater than 0')
        return price
