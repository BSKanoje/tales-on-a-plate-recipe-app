from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username


class Recipe(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    ingredients = models.TextField(help_text="List ingredients, one per line")
    instructions = models.TextField(help_text="Step-by-step instructions")
    cooking_time = models.PositiveIntegerField(help_text="Time in minutes")
    servings = models.CharField(max_length=20)
    image = models.ImageField(upload_to='recipes/')
    story = models.TextField(help_text="The story behind the recipe", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title


