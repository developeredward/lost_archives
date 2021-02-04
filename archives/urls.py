from django.urls import path
from .views import index, PostListView, PostDetailView, IndexView, search
import tinymce

urlpatterns = [
    path('home/', IndexView.as_view(), name='home'),
    path('', PostListView.as_view(), name='blog'),
    path('search/', search, name='search'),
    path('post/<pk>/', PostDetailView.as_view(), name='post-details'),
]
