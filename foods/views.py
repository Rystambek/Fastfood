from django.shortcuts import render, redirect
from .forms import NewFoodForm, FoodForm, FoodImageForm
from .models import FoodImage, Food
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
import os
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

@login_required(login_url='login')
def new_food(request):
    """
    View for creating a new Food object with multiple images.
    Handles both the main food data and additional images.
    """
    if request.method == "GET":
        form = NewFoodForm()
        image_form = FoodImageForm()
        return render(request, 'new_foods.html', {
            'form': form,
            'image_form': image_form
        })
    
    elif request.method == "POST":
        form = NewFoodForm(request.POST, request.FILES)
        image_form = FoodImageForm(request.POST, request.FILES)
        
        if form.is_valid():
            try:
                # Save the main food object
                food = form.save(request)
                
                # Handle additional images
                if 'images' in request.FILES:
                    for image in request.FILES.getlist('images'):
                        try:
                            FoodImage.objects.create(
                                image=image,
                                food=food
                            )
                        except ValidationError as e:
                            messages.warning(request, f"One or more images were invalid: {str(e)}")
                            continue
                
                messages.success(request, "Food item created successfully!")
                return redirect('main:index')
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
                return render(request, 'new_foods.html', {
                    'form': form,
                    'image_form': image_form
                })
        
        # If form is invalid, show errors
        return render(request, 'new_foods.html', {
            'form': form,
            'image_form': image_form
        })

def food_detail(request, food_id):
    """
    View for displaying food details and its images.
    """
    try:
        food = get_object_or_404(Food, id=food_id)
        similar_foods = Food.objects.filter(category=food.category).exclude(id=food.id)[:3]
        return render(request, 'details_food.html', {
            'food': food,
            'similar_foods': similar_foods
        })
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('main:index')

@login_required(login_url='login')
def food_update(request, food_id):
    """
    View for updating a food item and its images.
    Only accessible by superusers.
    """
    try:
        food = get_object_or_404(Food, id=food_id)
        
        if not request.user.is_superuser:
            messages.error(request, 'Access denied')
            return redirect('main:index')
        
        if request.method == 'GET':
            form = NewFoodForm(instance=food)
            image_form = FoodImageForm()
            return render(request, 'update_food.html', {
                'form': form,
                'image_form': image_form,
                'food': food
            })
        
        elif request.method == 'POST':
            form = NewFoodForm(request.POST, request.FILES, instance=food)
            if form.is_valid():
                form.save()
                
                # Handle additional images
                if 'images' in request.FILES:
                    try:
                        # Delete existing images if new ones are uploaded
                        FoodImage.objects.filter(food=food).delete()
                        for image in request.FILES.getlist('images'):
                            FoodImage.objects.create(
                                image=image,
                                food=food
                            )
                    except ValidationError as e:
                        messages.warning(request, f"One or more images were invalid: {str(e)}")
                
                messages.success(request, 'Food item updated successfully!')
                return redirect('main:index')
            
            return render(request, 'update_food.html', {
                'form': form,
                'food': food
            })
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('main:index')

@login_required(login_url='login')
def food_delete(request, food_id):
    """
    View for deleting a food item.
    Only accessible by superusers.
    """
    try:
        food = get_object_or_404(Food, id=food_id)
        
        if not request.user.is_superuser:
            messages.error(request, 'Access denied')
            return redirect('main:index')
        
        if request.method == 'POST':
            food.delete()
            messages.info(request, 'Food item deleted successfully!')
            return redirect('main:index')
        
        return render(request, 'delete_food.html', {'food': food})
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('main:index')

@require_http_methods(["POST"])
@csrf_exempt
def upload_images(request):
    """
    Handle AJAX file uploads.
    """
    if not request.user.is_authenticated:
        return JsonResponse({
            'success': False,
            'message': 'You must be logged in to upload images.'
        }, status=403)
    
    form = FoodImageForm(request.POST, request.FILES)
    
    if form.is_valid():
        try:
            # Get the food object (you'll need to pass this from the form)
            food_id = request.POST.get('food_id')
            if not food_id:
                return JsonResponse({
                    'success': False,
                    'message': 'Food ID is required.'
                }, status=400)
                
            food = Food.objects.get(id=food_id)
            
            # Save the images
            uploaded_files = []
            for image in form.cleaned_data['images']:
                food_image = FoodImage.objects.create(
                    food=food,
                    image=image
                )
                uploaded_files.append({
                    'name': image.name,
                    'url': food_image.image.url
                })
                
            return JsonResponse({
                'success': True,
                'message': f'Successfully uploaded {len(uploaded_files)} images.',
                'uploaded_files': uploaded_files
            })
            
        except Food.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Food not found.'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error uploading images: {str(e)}'
            }, status=500)
    else:
        return JsonResponse({
            'success': False,
            'message': 'Invalid form data.',
            'errors': form.errors
        }, status=400)