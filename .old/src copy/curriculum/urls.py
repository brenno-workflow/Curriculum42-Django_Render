# Criar um arquivo igual o 'urls.py' do projeto
from django.urls import path
from . import views

urlpatterns = [
    path('create/<int:id>', views.create, name='create'),
    path('update/<int:id>', views.update, name='update'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('list/<int:id>', views.list, name='list'),
    path('accessLevel/<int:id>', views.accessLevel, name='accessLevel'),
    path('published/<int:id>', views.published, name='published'),
    path('profile/<int:id>', views.profile, name='profile')
]

