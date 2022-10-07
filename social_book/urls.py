from django.urls import path
from . import views 

urlpatterns = [
    path('',views.index,name='index'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.logout, name='logout'),
    path('upload/', views.upload, name='upload'),
    path('settings/', views.settings, name='settings'),
    path('edit/<str:pk>/', views.edit_post,name='edit'),
    path('delete/<str:pk>/', views.delete_post, name='delete'),
    path('profile/<str:pk>/',views.profile, name='profile'),
    path('like-post', views.like_post, name='like_post'),
    
]
