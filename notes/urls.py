"""
URL patterns for notes app
"""
from django.urls import path
from . import views

app_name = 'notes'

urlpatterns = [
    # Dashboard and main views
    path('', views.DashboardView.as_view(), name='dashboard'),
    
    # Note CRUD operations
    path('note/create/', views.NoteCreateView.as_view(), name='note_create'),
    path('note/<uuid:pk>/', views.NoteDetailView.as_view(), name='note_detail'),
    path('note/<uuid:pk>/edit/', views.NoteUpdateView.as_view(), name='note_edit'),
    path('note/<uuid:pk>/delete/', views.NoteDeleteView.as_view(), name='note_delete'),
    
    # Category management
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('category/create/', views.CategoryCreateView.as_view(), name='category_create'),
    
    # AJAX endpoints
    path('ajax/note/<uuid:pk>/toggle-favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('ajax/note/<uuid:pk>/toggle-pin/', views.toggle_pin, name='toggle_pin'),
    path('ajax/search/', views.search_notes, name='search_notes'),
]
