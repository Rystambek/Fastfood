from django.db import models
from users.models import CustomUser
from django.core.validators import FileExtensionValidator
from django.utils.html import mark_safe
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('main:category', args=[self.name])

class Food(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=100000, decimal_places=2)
    phone_number = models.CharField(max_length=17)
    date = models.DateTimeField(auto_now_add=True)
    main_image = models.ImageField(upload_to='food_images', default='food_images/default.jpg')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)
    
    def image_tag(self):
        return mark_safe(f'<img src="{self.main_image.url}" width="150" height="150" />')
    
    image_tag.short_description = 'Image Preview'
    
    def get_absolute_url(self):
        return reverse('foods:detail', args=[self.id])
    
    class Meta:
        ordering = ['-id']
    

class FoodImage(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(
        upload_to='food_images',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])],
        help_text='Allowed formats: jpg, jpeg, png, gif',
        default='food_images/default.jpg'
    )

    def __str__(self):
        return f"Image for {self.food.title}"
    
    def image_tag(self):
        return mark_safe(f'<img src="{self.image.url}" width="150" height="150" />')
    
    image_tag.short_description = 'Image Preview'
    
class Comment(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    body = models.CharField(max_length=150)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return "Comment of" + str(self.author.username)
    
class Feedback(models.Model):
    food = models.ForeignKey('Food', on_delete=models.CASCADE, related_name='feedbacks')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.food.title}"