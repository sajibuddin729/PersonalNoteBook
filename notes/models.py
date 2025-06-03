"""
Models for notes, categories, and related functionality
"""
from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
import uuid
from core.utils import get_file_upload_path

User = get_user_model()

class Category(models.Model):
    """
    Category model for organizing notes
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#007bff', help_text='Hex color code')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        unique_together = ['name', 'user']
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('notes:category_detail', kwargs={'pk': self.pk})

class Tag(models.Model):
    """
    Simple tag model for notes
    """
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

class NoteTemplate(models.Model):
    """
    Template model for predefined note structures
    """
    TEMPLATE_TYPES = [
        ('meeting', 'Meeting Notes'),
        ('journal', 'Daily Journal'),
        ('task', 'Task List'),
        ('project', 'Project Planning'),
        ('idea', 'Idea Capture'),
        ('research', 'Research Notes'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    template_type = models.CharField(max_length=20, choices=TEMPLATE_TYPES)
    content = models.TextField(help_text='Template content with placeholders')
    description = models.TextField(blank=True)
    is_public = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='note_templates')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.get_template_type_display()})"

class Note(models.Model):
    """
    Main Note model
    """
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='notes')
    template = models.ForeignKey(NoteTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    is_pinned = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    is_favorite = models.BooleanField(default=False)
    reminder_date = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    shared_users = models.ManyToManyField(User, blank=True, related_name='shared_notes')
    tags = models.ManyToManyField(Tag, blank=True, related_name='notes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_pinned', '-updated_at']
        indexes = [
            models.Index(fields=['user', '-updated_at']),
            models.Index(fields=['user', 'is_pinned']),
            models.Index(fields=['user', 'is_favorite']),
        ]
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('notes:note_detail', kwargs={'pk': self.pk})
    
    @property
    def is_shared(self):
        return self.shared_users.exists()
    
    @property
    def word_count(self):
        return len(self.content.split())
    
    def get_tags_display(self):
        return ", ".join([tag.name for tag in self.tags.all()])

class NoteVersion(models.Model):
    """
    Model for storing note versions/history
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='versions')
    title = models.CharField(max_length=200)
    content = models.TextField()
    version_number = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['-version_number']
        unique_together = ['note', 'version_number']
    
    def __str__(self):
        return f"{self.note.title} - Version {self.version_number}"

class NoteAttachment(models.Model):
    """
    Model for note attachments (images, documents, etc.)
    """
    ATTACHMENT_TYPES = [
        ('image', 'Image'),
        ('document', 'Document'),
        ('audio', 'Audio'),
        ('video', 'Video'),
        ('other', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to=get_file_upload_path)
    file_name = models.CharField(max_length=255)
    file_size = models.PositiveIntegerField()
    file_type = models.CharField(max_length=10, choices=ATTACHMENT_TYPES)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.file_name} - {self.note.title}"
    
    @property
    def file_size_mb(self):
        return round(self.file_size / (1024 * 1024), 2)

class VoiceNote(models.Model):
    """
    Model for voice notes
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='voice_notes')
    audio_file = models.FileField(upload_to=get_file_upload_path)
    duration = models.PositiveIntegerField(help_text='Duration in seconds')
    transcription = models.TextField(blank=True, help_text='Auto-generated transcription')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Voice note for {self.note.title}"
    
    @property
    def duration_formatted(self):
        minutes = self.duration // 60
        seconds = self.duration % 60
        return f"{minutes}:{seconds:02d}"

class Drawing(models.Model):
    """
    Model for hand-drawn notes/sketches
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='drawings')
    image = models.ImageField(upload_to=get_file_upload_path)
    canvas_data = models.TextField(help_text='JSON data for canvas recreation')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Drawing for {self.note.title}"

class NoteShare(models.Model):
    """
    Model for managing note sharing permissions
    """
    PERMISSION_CHOICES = [
        ('view', 'View Only'),
        ('edit', 'Edit'),
        ('full', 'Full Access'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='shares')
    shared_with = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_shares')
    shared_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_shares')
    permission = models.CharField(max_length=10, choices=PERMISSION_CHOICES, default='view')
    shared_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['note', 'shared_with']
        ordering = ['-shared_at']
    
    def __str__(self):
        return f"{self.note.title} shared with {self.shared_with.full_name}"
