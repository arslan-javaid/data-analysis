from django.urls import path
from .views import Home, Authentication, LogoutView, RegisterView

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('login/', Authentication.as_view(), name='login'),
    path('accounts/login/', Authentication.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
]