from django.urls import path
from authen import views
from django.contrib.auth import views as auth_views

  
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('verify-email/', views.verify_email, name='verify_email'),
     path('password-reset/', views.ResetPasswordView.as_view(), name='password_reset'),

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),
         name='password_reset_confirm'),

    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
         name='password_reset_complete'),
    
]