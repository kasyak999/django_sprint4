from django.urls import path
from . import views


app_name = 'blog'
urlpatterns = [
    path('', views.IndexListView.as_view(), name='index'),
    path('posts/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path(
        'posts/<int:post_id>/edit/', views.PostUpdateView.as_view(),
        name='edit_post'
    ),
    path(
        'posts/create/', views.CreatingNewPostView.as_view(),
        name='create_post'
    ),
    path(
        'posts/<int:post_id>/delete/', views.PostUserDeleteView.as_view(),
        name='delete_post'
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
    path(
        'posts/<int:post_id>/comment/', views.AddCommentCreateView.as_view(),
        name='add_comment'
    ),
    path(
        'posts/<post_id>/edit_comment/<comment_id>/',
        views.EditCommentUpdateView.as_view(), name='edit_comment'
    ),
    path(
        'posts/<post_id>/delete_comment/<comment_id>/',
        views.CommentDeleteView.as_view(), name='delete_comment'
    )
]
