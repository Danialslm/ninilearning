from django.contrib.auth.views import LogoutView
from django.urls import path, include
from django.views.generic import RedirectView

from . import views

app_name = 'users'
urlpatterns = [
    path('', RedirectView.as_view(pattern_name='users:login')),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('signup/verification/', views.SignupVerificationView.as_view(), name='signup_verification'),
    path('signup/complete/', views.SignupConfirmView.as_view(), name='signup_complete'),
    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path(
        'password_reset/verification/',
        views.PasswordResetVerificationView.as_view(),
        name='password_reset_verification',
    ),
    path('password_reset/confirm/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    path('', include('apps.users.api.urls')),
]
