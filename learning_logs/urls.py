"""Define padrões de URL para learning_logs."""

from django.urls import path

from . import views

urlpatterns = [
    # Página inicial
    path('', views.index, name='index'),
    path('topics/', views.topics, name='topics'),
    path('topics/<int:pk>/', views.topic, name='topic'),
    path('topics/new/', views.new_topic, name='new_topic'),
    path('topics/<int:pk>/new_entry/', views.new_entry, name='new_entry'),
    path('topics/<int:topic_pk>/<int:entry_pk>/', views.edit_entry, name='edit_entry'),
]
