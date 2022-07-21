from django.urls import path

from . import views

urlpatterns = [
    path('send_code/', views.SendVerificationCodeAPIView.as_view(), name='send_verification_code'),
    path('revoke_session/', views.RevokeSessionAPIView.as_view(), name='revoke_session'),
]
