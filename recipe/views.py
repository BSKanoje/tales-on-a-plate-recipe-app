from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipe, UserProfile
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash


def about(request):
    return render(request, 'index.html')

@login_required(login_url='/login/')
def home(request):
    search_query = request.GET.get('search')
    if search_query:
        # Filter recipes based on the search query (case-insensitive)
        recipes = Recipe.objects.filter(title__icontains=search_query)
    else:
        # If no search query, display all recipes
        recipes = Recipe.objects.all()
    return render(request, 'home.html', {'recipes': recipes, 'search_query': search_query})


@login_required(login_url='/login/')
def recipes(request):
    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image')

        title = data.get("title")
        description = data.get("description")
        ingredients = data.get("ingredients")
        instructions = data.get("instructions")
        cooking_time = data.get("cooking_time")
        servings = data.get("servings")
        story = data.get("story")
        is_published = data.get("is_published") == 'on'

        Recipe.objects.create(
            title=title,
            description=description,
            ingredients=ingredients,
            instructions=instructions,
            cooking_time=cooking_time,
            servings=servings,
            image=image,
            story=story,
            author=request.user,
            is_published=is_published,
        )

        return redirect('/recipes/')

    queryset = Recipe.objects.all()

    if request.GET.get('search'):
        queryset = queryset.filter(title__icontains=request.GET.get('search'))

    context = {'recipes': queryset}
    return render(request, 'recipes.html', context)


@login_required(login_url='/login/')
def update_recipe(request, id):
    queryset = Recipe.objects.get(id=id)

    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image')

        queryset.title = data.get("title")
        queryset.description = data.get("description")
        queryset.ingredients = data.get("ingredients")
        queryset.instructions = data.get("instructions")
        queryset.cooking_time = data.get("cooking_time")
        queryset.servings = data.get("servings")
        queryset.story = data.get("story")
        queryset.is_published = data.get("is_published") == 'on'

        if image:
            queryset.image = image

        queryset.save()
        return redirect('/my-recipes/')

    context = {'recipe': queryset}
    return render(request, 'update_recipes.html', context)


@login_required(login_url='/login/')
def delete_recipe(request, id):
    queryset = Recipe.objects.get(id=id)
    queryset.delete()
    return redirect("/my-recipes/")


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request, "Invalid Username.")
            return redirect('/login/')

        user = authenticate(username=username, password=password)

        if user is None:
            messages.error(request, "Invalid Password.")
            return redirect('/login/')
        else:
            login(request, user)
            return redirect('/home/')

    return render(request, 'login.html')


def logout_page(request):
    logout(request)
    return redirect('/')


def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('/register/')

        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username
        )
        user.set_password(password)
        user.save()

        messages.success(request, "Account created successfully.")
        return redirect('/home/')

    return render(request, 'register.html')


def update_profile(request):
    return render(request, 'user_profile.html')


def recipe_detail(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    return render(request, 'recipe_detail.html', {'recipe': recipe})


@login_required
def my_recipes(request):
    recipes = Recipe.objects.filter(author=request.user)
    return render(request, 'my_recipes.html', {'recipes': recipes})

@login_required
def profile_view(request):
    return render(request, 'profile.html')


@login_required
def update_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        bio = request.POST.get('bio')
        location = request.POST.get('location')
        profile_picture = request.FILES.get('profile_picture')

        profile.bio = bio
        profile.location = location

        if profile_picture:
            profile.profile_picture = profile_picture

        profile.save()
        return redirect('profile')  # redirect to profile view

    return render(request, 'update_profile.html')


@login_required
def reset_password(request):
    if request.method == 'POST':
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('reset-password')  

        user = request.user
        user.set_password(new_password) 
        user.save()

        update_session_auth_hash(request, user)

        messages.success(request, "Password updated successfully.")

    return render(request, 'reset_password.html')