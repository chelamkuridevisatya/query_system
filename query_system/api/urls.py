from django.urls import path
from .views import QueryView, SignUpView, LoginView, RefreshTokenView,ForgotPasswordView, ResetPasswordView, home

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/<str:uidb64>/<str:token>/', ResetPasswordView.as_view(), name='reset-password'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('query/', QueryView.as_view(), name='query'),
    path('refresh-token/', RefreshTokenView.as_view(), name='refresh_token'),
    path('home/', home, name='home'),  # Optional home view
]
