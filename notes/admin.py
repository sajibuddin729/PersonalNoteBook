"""
Admin configuration for notes app
"""
from django.contrib import admin
from .models import (
    Note, Category, NoteTemplate, NoteVersion, 
    NoteAttachment, VoiceNote, Drawing, NoteShare
)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')

class NoteVersionInline(admin.TabularInline):
    model = NoteVersion
    extra = 0
    readonly_fields = ('created_at',)

class NoteAttachmentInline(admin.TabularInline):
    model = NoteAttachment
    extra = 0
    readonly_fields = ('uploaded_at', 'file_size')

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'priority', 'is_pinned', 'is_favorite', 'created_at')
    list_filter = ('priority', 'is_pinned', 'is_favorite', 'is_archived', 'created_at', 'category')
    search_fields = ('title', 'content', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('shared_users',)
    inlines = [NoteVersionInline, NoteAttachmentInline]
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'category')

@admin.register(NoteTemplate)
class NoteTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'template_type', 'user', 'is_public', 'created_at')
    list_filter = ('template_type', 'is_public', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at',)

@admin.register(NoteShare)
class NoteShareAdmin(admin.ModelAdmin):
    list_display = ('note', 'shared_with', 'shared_by', 'permission', 'shared_at', 'is_active')
    list_filter = ('permission', 'is_active', 'shared_at')
    search_fields = ('note__title', 'shared_with__email', 'shared_by__email')
    readonly_fields = ('shared_at',)

@admin.register(VoiceNote)
class VoiceNoteAdmin(admin.ModelAdmin):
    list_display = ('note', 'duration_formatted', 'created_by', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('note__title', 'transcription')
    readonly_fields = ('created_at',)

@admin.register(Drawing)
class DrawingAdmin(admin.ModelAdmin):
    list_display = ('note', 'created_by', 'created_at')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)
