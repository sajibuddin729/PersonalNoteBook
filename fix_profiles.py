#!/usr/bin/env python
"""
Script to fix user profile issues
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notebook_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from accounts.models import UserProfile

User = get_user_model()

def fix_user_profiles():
    """Fix user profile issues"""
    print("🔧 Fixing user profile issues...")
    
    # Get all users
    users = User.objects.all()
    fixed_count = 0
    
    for user in users:
        try:
            # Try to get the profile
            profile = user.profile
            if not profile.user:
                profile.user = user
                profile.save()
                print(f"✅ Fixed profile for user: {user.email}")
                fixed_count += 1
        except UserProfile.DoesNotExist:
            # Create missing profile
            UserProfile.objects.create(user=user)
            print(f"✅ Created profile for user: {user.email}")
            fixed_count += 1
    
    if fixed_count == 0:
        print("✅ All user profiles are already correct!")
    else:
        print(f"✅ Fixed {fixed_count} user profiles")

if __name__ == '__main__':
    fix_user_profiles()
