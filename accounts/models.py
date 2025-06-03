"""
User models and profile management
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
import uuid
import os

def get_avatar_upload_path(instance, filename):
    """Generate upload path for user avatars"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('avatars', str(instance.user.id), filename)

class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        db_table = 'auth_user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
    
    def get_absolute_url(self):
        return reverse('accounts:profile')
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    def get_or_create_profile(self):
        """Get or create user profile"""
        try:
            return self.profile
        except UserProfile.DoesNotExist:
            return UserProfile.objects.create(user=self)

class UserProfile(models.Model):
    """
    Extended user profile information
    """
    THEME_CHOICES = [
        ('light', 'Light'),
        ('dark', 'Dark'),
        ('auto', 'Auto'),
    ]
    
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='profile',
        null=False,  # Ensure user is always required
        blank=False
    )
    bio = models.TextField(max_length=500, blank=True)
    # Using ImageField now that Pillow is installed
    avatar = models.ImageField(upload_to=get_avatar_upload_path, blank=True, null=True)
    # Keep avatar_url for backward compatibility
    avatar_url = models.URLField(blank=True, help_text='URL to your avatar image (legacy)')
    phone_number = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    theme_preference = models.CharField(max_length=10, choices=THEME_CHOICES, default='light')
    email_notifications = models.BooleanField(default=True)
    desktop_notifications = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
    
    def __str__(self):
        return f"{self.user.full_name}'s Profile"
    
    @property
    def get_avatar(self):
        """Return avatar URL or default"""
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        elif self.avatar_url:
            return self.avatar_url
        return '/static/images/default-avatar.png'
    
    def save(self, *args, **kwargs):
        """Override save to ensure user is set"""
        if not self.user_id:
            raise ValueError("UserProfile must have a user")
        super().save(*args, **kwargs)
