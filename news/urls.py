from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.post_list, name='post_list'), 

    path('post/<int:post_id>/', views.post_detail, name='post_detail'), 
    path('post/create/', views.post_create, name='post_create'),
    path('post/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('vote/<int:post_id>/<str:vote_type>/', views.vote, name='vote'),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('popular/', views.popular_posts, name='popular_posts'),  

    path('categories/', views.category_list, name='category_list'),  
    path('category/<int:category_id>/', views.category_posts, name='category_posts'),  
    path('category/create/', views.category_create, name='category_create'),  
    path('category/<int:category_id>/edit/', views.category_edit, name='category_edit'),
    path('category/<int:category_id>/delete/', views.category_delete, name='category_delete'),

    path('profile/<str:username>/', views.profile, name='profile'),  

    path('login/', views.login_view, name='login'),
    path('accounts/login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
