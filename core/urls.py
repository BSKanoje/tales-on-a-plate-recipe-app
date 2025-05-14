"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from recipe.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', include('recipe.urls')),

    path('', about, name='about'),
    path('login/', login_page, name='login_page'),
    path('register/', register, name='register'),
    path('recipes/', recipes, name='recipes'),
    path('logout/', logout_page, name='logout_page'),
    path('delete-recipe/<id>/', delete_recipe, name="delete_recipe"),
    path('update-recipe/<id>/', update_recipe, name="update_recipe"),
    path('profile/', update_profile, name='profile'),
    path('recipe/<int:id>/', recipe_detail, name='recipe_detail'), 

    path('my-recipes/', my_recipes, name='my_recipes'),
  

    path('home/', home, name='home'),

    path('update-profile/', update_profile, name="update_profile"),
    path('profile/', profile_view, name='profile'),  # for displaying profile
    path('reset-password/', reset_password, name='reset-password'),


    path('admin/', admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    
urlpatterns += staticfiles_urlpatterns()