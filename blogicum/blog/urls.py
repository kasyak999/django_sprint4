from django.urls import path
from . import views


app_name = 'blog'
urlpatterns = [
    path('', views.IndexListView.as_view(), name='index'),
    path('posts/<int:pk>/', views.post_detail, name='post_detail'),
    path(
        'posts/<int:post_id>/edit/', views.PostUpdateView.as_view(), 
        name='edit_post'
    ),
    path(
        'category/<slug:category_slug>/',
        views.CategoryPostsListView.as_view(), name='category_posts'
    ),
    path(
        'profile/<str:username>/', views.ProfileDetailView.as_view(),
        name='profile'
    ),
    path(
        'edit/', views.ProfileUpdateView.as_view(), name='edit_profile'
    ),
    path('posts/create/', views.CreateCreateView.as_view(), name='create_post')
]
