"""
Views for notes management
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.db.models import Q, Count
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.utils import timezone
from core.mixins import UserOwnershipMixin, NoteOwnershipMixin
from .models import Note, Category, NoteTemplate, NoteShare, NoteVersion
from .forms import NoteForm, CategoryForm, NoteTemplateForm, NoteShareForm, SearchForm

class DashboardView(LoginRequiredMixin, ListView):
    """
    Main dashboard view showing user's notes
    """
    model = Note
    template_name = 'notes/dashboard.html'
    context_object_name = 'notes'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Note.objects.filter(
            Q(user=self.request.user) | Q(shared_users=self.request.user)
        ).distinct().select_related('category', 'user').prefetch_related('tags')
        
        # Filter by search query
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(tags__name__icontains=search_query)
            ).distinct()
        
        # Filter by category
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        # Filter by priority
        priority = self.request.GET.get('priority')
        if priority:
            queryset = queryset.filter(priority=priority)
        
        # Filter by favorites
        if self.request.GET.get('favorites'):
            queryset = queryset.filter(is_favorite=True)
        
        # Filter by pinned
        if self.request.GET.get('pinned'):
            queryset = queryset.filter(is_pinned=True)
        
        return queryset.filter(is_archived=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(user=self.request.user)
        context['search_form'] = SearchForm(user=self.request.user, data=self.request.GET)
        context['total_notes'] = Note.objects.filter(user=self.request.user).count()
        context['pinned_notes'] = Note.objects.filter(user=self.request.user, is_pinned=True).count()
        context['favorite_notes'] = Note.objects.filter(user=self.request.user, is_favorite=True).count()
        context['recent_notes'] = Note.objects.filter(user=self.request.user).order_by('-updated_at')[:5]
        return context

class NoteDetailView(NoteOwnershipMixin, DetailView):
    """
    Detailed view of a single note
    """
    model = Note
    template_name = 'notes/note_detail.html'
    context_object_name = 'note'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['versions'] = self.object.versions.all()[:10]
        context['attachments'] = self.object.attachments.all()
        context['voice_notes'] = self.object.voice_notes.all()
        # context['drawings'] = self.object.drawings.all()  # Commented out until Pillow is installed
        context['shares'] = self.object.shares.filter(is_active=True)
        return context

class NoteCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new note
    """
    model = Note
    form_class = NoteForm
    template_name = 'notes/note_form.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        
        # Create initial version
        NoteVersion.objects.create(
            note=self.object,
            title=self.object.title,
            content=self.object.content,
            version_number=1,
            created_by=self.request.user
        )
        
        messages.success(self.request, f'Note "{self.object.title}" created successfully!')
        
        # Check if user wants to continue editing
        if 'save_and_continue' in self.request.POST:
            return redirect('notes:note_edit', pk=self.object.pk)
        
        return response

class NoteUpdateView(NoteOwnershipMixin, UpdateView):
    """
    Update an existing note
    """
    model = Note
    form_class = NoteForm
    template_name = 'notes/note_form.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        # Create new version if content changed
        if form.has_changed() and ('title' in form.changed_data or 'content' in form.changed_data):
            last_version = self.object.versions.first()
            version_number = last_version.version_number + 1 if last_version else 1
            
            NoteVersion.objects.create(
                note=self.object,
                title=form.cleaned_data['title'],
                content=form.cleaned_data['content'],
                version_number=version_number,
                created_by=self.request.user
            )
        
        response = super().form_valid(form)
        messages.success(self.request, f'Note "{self.object.title}" updated successfully!')
        
        if 'save_and_continue' in self.request.POST:
            return redirect('notes:note_edit', pk=self.object.pk)
        
        return response

class NoteDeleteView(NoteOwnershipMixin, DeleteView):
    """
    Delete a note
    """
    model = Note
    template_name = 'notes/note_confirm_delete.html'
    success_url = reverse_lazy('notes:dashboard')
    
    def delete(self, request, *args, **kwargs):
        note_title = self.get_object().title
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f'Note "{note_title}" deleted successfully!')
        return response

class CategoryListView(UserOwnershipMixin, ListView):
    """
    List all categories for the user
    """
    model = Category
    template_name = 'notes/category_list.html'
    context_object_name = 'categories'
    
    def get_queryset(self):
        return super().get_queryset().annotate(note_count=Count('notes'))

class CategoryCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new category
    """
    model = Category
    form_class = CategoryForm
    template_name = 'notes/category_form.html'
    success_url = reverse_lazy('notes:category_list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, f'Category "{self.object.name}" created successfully!')
        return response

# AJAX Views
@login_required
def toggle_favorite(request, pk):
    """
    Toggle favorite status of a note via AJAX
    """
    note = get_object_or_404(Note, pk=pk, user=request.user)
    note.is_favorite = not note.is_favorite
    note.save()
    
    return JsonResponse({
        'success': True,
        'is_favorite': note.is_favorite,
        'message': 'Added to favorites' if note.is_favorite else 'Removed from favorites'
    })

@login_required
def toggle_pin(request, pk):
    """
    Toggle pin status of a note via AJAX
    """
    note = get_object_or_404(Note, pk=pk, user=request.user)
    note.is_pinned = not note.is_pinned
    note.save()
    
    return JsonResponse({
        'success': True,
        'is_pinned': note.is_pinned,
        'message': 'Note pinned' if note.is_pinned else 'Note unpinned'
    })

@login_required
def search_notes(request):
    """
    AJAX search for notes
    """
    query = request.GET.get('q', '')
    if len(query) < 2:
        return JsonResponse({'results': []})
    
    notes = Note.objects.filter(
        Q(user=request.user) | Q(shared_users=request.user),
        Q(title__icontains=query) | Q(content__icontains=query) | Q(tags__name__icontains=query)
    ).distinct()[:10]
    
    results = []
    for note in notes:
        results.append({
            'id': str(note.id),
            'title': note.title,
            'content_preview': note.content[:100] + '...' if len(note.content) > 100 else note.content,
            'url': note.get_absolute_url(),
            'category': note.category.name if note.category else None,
            'updated_at': note.updated_at.strftime('%Y-%m-%d %H:%M')
        })
    
    return JsonResponse({'results': results})
