from django.urls import path
from . import views


app_name = 'blog'
urlpatterns = [
    path('', views.IndexListView.as_view(), name='index'),
    path('posts/<int:pk>/', views.post_detail, name='post_detail'),
    # path(
    #     'category/<slug:category_slug>/',
    #     views.category_posts, name='category_posts'
    # ),
    path(
        'category/<slug:category_slug>/',
        views.CategoryPostsListView.as_view(), name='category_posts'
    ),
    path(
        'profile/<str:username>/', views.ProfileDetailView.as_view(),
        name='profile'
    ),
    path(
        'edit', views.ProfileUpdateView.as_view(), name='edit_profile'
    ),
]
