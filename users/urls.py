# users/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    # --- THIS IS THE LINE THAT FIXES THE 404 ERROR ---
    # When a user visits the root of the site, show the login view.
    # We can give it a new name, like 'home', or just reuse 'login'.
    path('', views.login_view, name='home'), 

    # Your other URLs remain the same
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'), # It's okay to have two URLs point to the same view
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('profile/', views.profile_view, name='profile'),
    
    path(
        'password_change/',
        auth_views.PasswordChangeView.as_view(
            template_name='users/password_change.html',
            success_url='/password_change/done/' 
        ),
        name='password_change'
    ),
    path(
        'password_change/done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='users/password_change_done.html'
        ),
        name='password_change_done'
    ),
]