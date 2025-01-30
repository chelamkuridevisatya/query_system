from django.urls import path
from .views import QueryView, SignUpView, LoginView, RefreshTokenView, home

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('query/', QueryView.as_view(), name='query'),
    path('refresh-token/', RefreshTokenView.as_view(), name='refresh_token'),
    path('home/', home, name='home'),  # Optional home view
]
