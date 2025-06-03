"""
Forms for note creation and management
"""
from django import forms
from django.contrib.auth import get_user_model
from django.db import models  # Add this import
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field, Div, HTML
from .models import Note, Category, NoteTemplate, NoteShare, Tag

User = get_user_model()

class NoteForm(forms.ModelForm):
    """
    Form for creating and editing notes
    """
    tags_input = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Enter tags separated by commas'}),
        help_text='Enter tags separated by commas (e.g., work, important, project)'
    )
    
    class Meta:
        model = Note
        fields = ['title', 'content', 'category', 'template', 'priority', 'is_pinned', 
                 'is_favorite', 'reminder_date']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 15, 'id': 'note-editor'}),
            'reminder_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            self.fields['category'].queryset = Category.objects.filter(user=user)
            self.fields['template'].queryset = NoteTemplate.objects.filter(
                models.Q(user=user) | models.Q(is_public=True)
            )
        
        # Pre-populate tags if editing
        if self.instance.pk:
            tags = self.instance.tags.all()
            self.fields['tags_input'].initial = ', '.join([tag.name for tag in tags])
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('title', css_class='form-control mb-3', placeholder='Enter note title'),
            Row(
                Column('category', css_class='form-group col-md-4 mb-3'),
                Column('template', css_class='form-group col-md-4 mb-3'),
                Column('priority', css_class='form-group col-md-4 mb-3'),
                css_class='form-row'
            ),
            Field('content', css_class='form-control mb-3'),
            Field('tags_input', css_class='form-control mb-3'),
            Field('reminder_date', css_class='form-control mb-3'),
            Row(
                Column('is_pinned', css_class='form-group col-md-4 mb-3'),
                Column('is_favorite', css_class='form-group col-md-4 mb-3'),
                css_class='form-row'
            ),
            Div(
                Submit('save', 'Save Note', css_class='btn btn-primary me-2'),
                Submit('save_and_continue', 'Save & Continue Editing', css_class='btn btn-secondary'),
                css_class='d-flex gap-2'
            )
        )
    
    def save(self, commit=True):
        note = super().save(commit=commit)
        
        if commit:
            # Handle tags
            tags_input = self.cleaned_data.get('tags_input', '')
            if tags_input:
                tag_names = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
                note.tags.clear()
                for tag_name in tag_names:
                    tag, created = Tag.objects.get_or_create(name=tag_name.lower())
                    note.tags.add(tag)
        
        return note

class CategoryForm(forms.ModelForm):
    """
    Form for creating and editing categories
    """
    class Meta:
        model = Category
        fields = ['name', 'description', 'color']
        widgets = {
            'color': forms.TextInput(attrs={'type': 'color'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('name', css_class='form-control mb-3'),
            Field('description', css_class='form-control mb-3'),
            Field('color', css_class='form-control mb-3'),
            Submit('submit', 'Save Category', css_class='btn btn-primary')
        )

class NoteTemplateForm(forms.ModelForm):
    """
    Form for creating note templates
    """
    class Meta:
        model = NoteTemplate
        fields = ['name', 'template_type', 'content', 'description', 'is_public']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-8 mb-3'),
                Column('template_type', css_class='form-group col-md-4 mb-3'),
                css_class='form-row'
            ),
            Field('description', css_class='form-control mb-3'),
            Field('content', css_class='form-control mb-3'),
            Field('is_public', css_class='form-check mb-3'),
            Submit('submit', 'Save Template', css_class='btn btn-primary')
        )

class NoteShareForm(forms.ModelForm):
    """
    Form for sharing notes with other users
    """
    shared_with = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Select a user to share with"
    )
    
    class Meta:
        model = NoteShare
        fields = ['shared_with', 'permission', 'expires_at']
        widgets = {
            'expires_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            # Exclude the current user from the sharing options
            self.fields['shared_with'].queryset = User.objects.exclude(id=user.id)
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('shared_with', css_class='form-control mb-3'),
            Field('permission', css_class='form-control mb-3'),
            Field('expires_at', css_class='form-control mb-3'),
            Submit('submit', 'Share Note', css_class='btn btn-primary')
        )

class SearchForm(forms.Form):
    """
    Form for searching notes
    """
    query = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search notes, tags, or content...',
            'id': 'search-input'
        })
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.none(),
        required=False,
        empty_label="All Categories",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    priority = forms.ChoiceField(
        choices=[('', 'All Priorities')] + Note.PRIORITY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            self.fields['category'].queryset = Category.objects.filter(user=user)
