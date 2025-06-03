"""
Views for user authentication and profile management
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm, UserUpdateForm
from .models import User, UserProfile

class CustomLoginView(LoginView):
    """
    Custom login view with enhanced styling
    """
    form_class = CustomAuthenticationForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('notes:dashboard')
    
    def form_valid(self, form):
        messages.success(self.request, f'Welcome back, {form.get_user().first_name}!')
        return super().form_valid(form)

class CustomLogoutView(LogoutView):
    """
    Custom logout view
    """
    template_name = 'accounts/logout.html'
    
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, 'You have been successfully logged out.')
        return super().dispatch(request, *args, **kwargs)

class RegisterView(CreateView):
    """
    User registration view
    """
    model = User
    form_class = CustomUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('notes:dashboard')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        messages.success(self.request, f'Welcome to Personal Notebook, {user.first_name}!')
        return response
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('notes:dashboard')
        return super().dispatch(request, *args, **kwargs)

class ProfileView(LoginRequiredMixin, UpdateView):
    """
    User profile view and update
    """
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('accounts:profile')
    
    def get_object(self, queryset=None):
        """
        Get or create the user profile, ensuring proper user relationship
        """
        try:
            # Try to get existing profile
            profile = UserProfile.objects.get(user=self.request.user)
        except UserProfile.DoesNotExist:
            # Create new profile if it doesn't exist
            profile = UserProfile.objects.create(user=self.request.user)
        
        # Ensure the profile has the correct user (fix any orphaned profiles)
        if not profile.user:
            profile.user = self.request.user
            profile.save()
        
        return profile
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserUpdateForm(instance=self.request.user)
        # Add favorite notes count to context
        try:
            context['favorite_notes_count'] = self.request.user.notes.filter(is_favorite=True).count()
        except:
            context['favorite_notes_count'] = 0
        return context
    
    def form_valid(self, form):
        # Ensure the profile is associated with the current user
        form.instance.user = self.request.user
        
        # Handle file upload
        if 'avatar' in self.request.FILES:
            form.instance.avatar = self.request.FILES['avatar']
        
        messages.success(self.request, 'Your profile has been updated successfully!')
        return super().form_valid(form)

@login_required
def update_user_info(request):
    """
    Update basic user information
    """
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your information has been updated successfully!')
            return redirect('accounts:profile')
    return redirect('accounts:profile')
