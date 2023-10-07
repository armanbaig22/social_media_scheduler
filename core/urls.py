from django.urls import path
from . import views


urlpatterns = [
    path('', views.frontpage, name='frontpage'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('linkedin-auth/', views.linkedin_auth, name='linkedin_auth'),
    path('auth/linkedin/callback/', views.linkedin_callback, name='linkedin_callback'),
    path('profile/', views.profile, name='profile'),
]
