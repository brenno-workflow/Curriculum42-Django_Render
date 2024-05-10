# Criar um arquivo igual o 'urls.py' do projeto
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('create/<int:id>', views.create, name='create'),
    path('update/<int:id>', views.update, name='update'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('list/<int:id>', views.list, name='list'),
    path('accessLevel/<int:id>', views.accessLevel, name='accessLevel'),
    path('published/<int:id>', views.published, name='published'),
    path('profile/<int:id>', views.profile, name='profile'),
    re_path('create_key/(?P<id>\d+)/$', views.create_key, name='create_key'),
    re_path('profile_key/(?P<id>\d+)/$', views.profile_key, name='profile_key'),
    re_path('update_key/(?P<id>\d+)/$', views.update_key, name='update_key'),
    re_path('delete_key/(?P<id>\d+)/$', views.delete_key, name='delete_key')
]

